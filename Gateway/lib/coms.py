from network import WLAN
from network import LoRa
from machine import RTC
import machine
import socket
import utime

class C_Wifi:

    def __init__(self, networks):
        print('[Wifi] Wifi starting...')
        self.wlan = WLAN(mode=STA)
        nets = self.wlan.scan()
        for net in nets:
            if self.wlan.isconnected():
                break
            utime.sleep_ms(10000)
            for network in networks:
                if net.ssid == network[1]:
                    if network[0] == 'WPA2':
                        self.wlan.connect(network[1], auth=(WLAN.WPA2, network[2]), timeout=10000)
                    elif network[0] == 'WPA2E':
                        self.wlan.connect(network[1], auth=(WLAN.WPA2_ENT, network[3], network[2]), identity=network[3], timeout=10000)
                    break
        if not self.wlan.isconnected():
            machine.reset()
            break
        print('[Wifi] Wifi started')

class C_LoRa:

    def __init__(self):
        print('[LoRa] LoRa socket starting...')
        self.lora = LoRa(mode=LoRa.LORA, region=LpRa.EU868)
        self.lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.lora_socket.setblocking(False)
        print('[LoRa] LoRa socket started')

class C_RTC:

    def __init__(self):
        print('[RTC] RTC sync in progress...')
        self.rtc = RTC()
        self.ntp_sync("pool.ntp.org")
        print('[RTC] RTC synced')

