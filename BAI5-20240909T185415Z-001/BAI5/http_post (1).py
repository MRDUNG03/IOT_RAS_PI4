import paho.mqtt.client as mqtt
from seeed_dht import DHT
from grove.grove_relay import GroveRelay
import json
# ===================================
# khai bao thu vien
from time import sleep, strftime
from urllib import request
import random as rd

# khai bao thiet bi
# lcd=LCD()
dht = DHT("11",4)

# khai bao channel 
channel_ID = "2643589"


def post_http():
    api_key = "691SFL628MORIGS1"
    url = "https://api.thingspeak.com/update?api_key=%s&field2=%s&field1=%s" %(api_key,temp,humi)
    request.urlopen(url)
    r=request.urlopen(url)
    print("http send ok ")

while True:
    humi, temp = dht.read()
    print("Temp: {}C, Humi: {}%".format(temp, humi))
    h,m,s = strftime("%H:%M:%S").split(":")
    print(strftime("%H:%M:%S"), end= " : ")
    # lcd.setCursor(0,0)
    # lcd.write("Time: {}:{}  ".format(h,m))
    post_http()
    sleep(15)
    
