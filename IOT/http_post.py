import paho.mqtt.client as mqtt
from seeed_dht import DHT
from grove.grove_relay import GroveRelay
import json
# ===================================
# khai bao thu vien
from time import sleep, strftime
from urllib import request
import random as rd
from grove.display.jhd1802 import JHD1802

# khai bao thiet bi
lcd =JHD1802()
dht = DHT("11",5)

# khai bao channel 
channel_ID = "2643589"


def post_http():
    api_key = "691SFL628MORIGS1"
    url = "https://api.thingspeak.com/update?api_key=%s&field2=%s&field1=%s" %(api_key,temp,humi)
    request.urlopen(url)
    r=request.urlopen(url)
    print("http send ok ")

while True:
    try :
        humi, temp = dht.read()
        print("Temp: {}C, Humi: {}%".format(temp, humi))
        h,m,s = strftime("%H:%M:%S").split(":")
        print(strftime("%H:%M:%S"), end= " : ")
        lcd.setCursor(0,0)
        lcd.write("Time: {}:{}  ".format(h,m))
        post_http()
        sleep(15)
    except:
        print("no connected")
        sleep(2)        
    
