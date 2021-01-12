#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from network import LoRa
import socket
import crypto
import utime
import _thread
import pycom
import SDmount
import CONFIG as cfg
from MQ131_O3_Sensor import MQ131
from MiCs6814_MultiChannel_Sensor import MiCS6814
from SEN0219_CO2_Sensor import SEN0219
from SEN0219_CO2_Sensor import SEN0219_SERIAL
from PMS5003ST_Sensor import PMS5003ST
from machine import RTC

keycode = cfg.keycode
R0_MQ131 = cfg.R0_MQ131
sleep_lenght = const(450)

rtc = RTC()
rtc.init((cfg.RTC["Ano"], cfg.RTC["Mes"], cfg.RTC["Dia"], cfg.RTC["Hora"], cfg.RTC["Minutos"], cfg.RTC["Segundos"], 0, 0))

lora = LoRa(mode=LoRa.LORA, frequency=863000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def _Random():
   r = crypto.getrandbits(32)
   return ((r[0]<<24)+(r[1]<<16)+(r[2]<<8)+r[3])/4294967295.0

def _RandomRange(rfrom, rto):
   return _Random()*(rto-rfrom)+rfrom

def th_send(data, id):
    while True:
        try:
            #SDmount.check('/sd') #em Thread, usar trincos
            pycom.rgbled(0x0000ff) #Blue

            #   MiCS 6814

            print('MiCS')
            MiCS = MiCS6814(SDA='P10',SCL='P11')
            utime.sleep(1)
            gases=MiCS.calcAllGases()
            MiCS.deinit()
            # # f = open('/sd/Log_MiCS.csv', 'a')
            # # f.write("\""+str(utime.gmtime())+"\";\""+str(gases[0])+"\";\""+str(gases[1])+"\";\""+str(gases[2])+"\";\""+str(gases[3])+"\";\""+str(gases[4])+"\";\""+str(gases[5])+"\";\""+str(gases[6])+"\";\""+str(gases[7])+"\"\n")
            # # f.close()
            NO2=str(gases[1]); #Possui mais gases mas só queremos o NO2
            #NO2=str(_RandomRange(0.05, 10));

            pycom.rgbled(0xe042f5) #Purple
            #   MQ 131

            print('MQ')
            MQ = MQ131(pin='P18', R0=R0_MQ131)
            utime.sleep(1)
            MQvolts = MQ.MQRead()
            MQPPB = MQ.MQGet_PPB(MQvolts)
            MQ.deinit()
            # # f = open('/sd/Log_MQ.csv', 'a')
            # # f.write("\""+str(utime.gmtime())+"\";\""+str(MQPPB)+"\";\""+str(MQvolts)+"\"\n")
            # # f.close()
            O3=str(MQPPB)
            # O3=str(_RandomRange(0, 10));

            pycom.rgbled(0x00ff00) #Green
            # PMS5003ST

            print('PMS')
            PMS = PMS5003ST(TX='P3', RX='P21')
            utime.sleep(1)
            PMSdata = PMS.PMSReadActive()
            PMS.deinit()
            if(PMSdata==False):
                pycom.rgbled(0xffff00)
                print('PMS failed to Read')
                continue
            # # #     print('PMS error')
            # # # f = open('/sd/Log_PMS.csv', 'a')
            # # # f.write("\""+str(utime.gmtime())+"\";\""+str(PMSdata[12])+"\";\""+str(PMSdata[13])+"\";\""+str(PMSdata[14])+"\"\n")
            # # # f.close()
            CH2O_PPM=(24.45 * PMSdata[12]) / 30.026
            CH2O=str(CH2O_PPM)
            Temp=str(PMSdata[13])
            Humd=str(PMSdata[14])
            # CH2O=str(_RandomRange(0, 10));
            # Temp=str(_RandomRange(15, 25));
            # Humd=str(_RandomRange(40, 70));

            #   SEN 0219


            pycom.rgbled(0xe042f5) #Purple
            #SEN = SEN0219(pin='P17', offset=0)
            print('SEN')
            SEN_S = SEN0219_SERIAL(TX='P22', RX='P23')
            #SEN_S.SEN_Serial_ABCOn()
            utime.sleep(1)
            SENdata = SEN_S.SEN_Serial_read()
            SEN_S.deinit()
            #SENvolts = SEN.SENRead()
            #SENPPM = SEN.SENGet_PPM(SENvolts)
            #SEN.deinit()
            SEN_S.deinit()
            #if(SENPPM==False):
            if(SENdata==False):
                pycom.rgbled(0xffff00)
                print('SEN error (preheating?)')
                continue
            SENPPM = (256*SENdata[2]) + SENdata[3]
            # f = open('/sd/Log_SEN.csv', 'a')
            # f.write("\""+str(utime.gmtime())+"\";\""+str(SENPPM)+"\"\n")
            # f.close()
            CO2=str(SENPPM)
            # CO2=str(_RandomRange(390, 2000));
            print('Data')
            data = '{"keycode": "'+keycode+'","CO2": '+CO2+',"NO2": '+NO2+',"O3": '+O3+',"CH2O": '+CH2O+',"Temp": '+Temp+',"Humd": '+Humd+'}'
            print(str(rtc.now())+data)

            s.send(data)

            # print("Save Localy")
            #
            # f = open('/sd/DataLog.csv', 'a')
            #
            # f.write("\""+str(rtc.now())+";"+data+"\"\n")
            # f.close()

            pycom.rgbled(0x000000) # off
            utime.sleep(sleep_lenght)
        except Exception as e:
            import sys
            pycom.rgbled(0xff0000) # red
            print("exception")
            with open("error.log", "a") as f:
                sys.print_exception(e, f)

pycom.heartbeat(False)
_thread.start_new_thread(th_send, (0, 0))
