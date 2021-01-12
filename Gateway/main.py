from network import LoRa
from network import WLAN
from machine import RTC
import socket
import utime
import binascii
import crypto
import _thread
import urequests
import pycom
import machine
import CONFIG as config

#Wlan
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
# print(len(nets))
for net in nets:
    if wlan.isconnected():
        break
    utime.sleep_ms(10000)
    for network in config.networks:
        if net.ssid == network[1]:
            # print("Testing: "+network[1])
            if network[0] == 'WPA2':
                wlan.connect(network[1], auth=(WLAN.WPA2, network[2]), timeout=10000)
            elif network[0] == 'WPA2E':
                wlan.connect(network[1], auth=(WLAN.WPA2_ENT, network[3], network[2]), identity=network[3], timeout=10000)
            break

if not wlan.isconnected():
    machine.reset()

#RTC
rtc = RTC()
rtc.ntp_sync("pool.ntp.org")
print('RTC synced')

#LoRa

lora = LoRa(mode=LoRa.LORA, frequency=863000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def _encryptor(data):
    #RSA Encryption - 2048 bits & PKCS8 followed by base64 binary to ascii convertion
    f = open(config.publicKeyCert)
    pk = f.read()
    f.close()
    msg = str(binascii.b2a_base64(crypto.rsa_encrypt(data, pk)))
    payload='{"msg": "'+msg+'"}'
    return payload

def th_send(data, id):
    for i in range(5):  #5 attempts
        try:
            pycom.rgbled(0x0000ff) # blue
            payload=_encryptor(data)
            res = urequests.post(config.url,headers=config.headers, data=payload)
            if res.status_code == 200:
                res.close()
                pycom.rgbled(0x000000) # off
                return
            else:
                res.close()
        except Exception as e:
            import sys
            pycom.rgbled(0xff0000) # red
            with open("error.log", "a") as f:
                sys.print_exception(e, f)

#def th_rtc(data, id):
#    s.send('{"RTC": "'+str(rtc.now())+'"}')

pycom.heartbeat(False)
while True:
    try:
        if not wlan.isconnected():
            machine.reset()
        data = s.recv(256)
        if data:
            pycom.rgbled(0x00ff00) # green
            data=str(data)[2:-1]

            print(data)
            # if data is rtc do th_rtc else do th_send
            # usar filas de entrada e saida

            _thread.start_new_thread(th_send, (data, 0))
        utime.sleep(1)
    except Exception as e:
        import sys
        pycom.rgbled(0xff0000) # red
        with open("error.log", "a") as f:
            sys.print_exception(e, f)
