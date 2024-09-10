import paho.mqtt.client as mqtt
from urllib import request, parse
from gpiozero import LED
from gpiozero import Buzzer
from grove.grove_relay import GroveRelay
import time
import json
import datetime

#khai bao chan GPIO MODULE
led = LED(24)
buzzer = Buzzer(16)
relay = GroveRelay(26)
#KHAI BAO ID CHANEL -- API_READ

apiKeyRead = "0FICQRIHXPHRENQB"
channelID = "2643589"

#HAM DOC DATA TU THINGSPEAK
#HAM DOC NHIET DO 
def getTEMP():
    req=request.Request("https://api.thingspeak.com/channels/%s/fields/2/last.json?api_key=%s"%(channelID,apiKeyRead),method="GET")
    r = request.urlopen(req)
    respone_data=r.read().decode()
    respone_data=json.loads(respone_data)
    print(respone_data)
    field2 = respone_data['field2']
    print(field2)
    return field2
#HAM DOC DO AM 
def getHumi():
    req=request.Request("https://api.thingspeak.com/channels/%s/fields/1/last.json?api_key=%s"%(channelID,apiKeyRead),method="GET")
    r = request.urlopen(req)
    respone_data=r.read().decode()
    respone_data=json.loads(respone_data)
    field1 = respone_data['field1']
    return field1
# HAM DOC TRANG THAI BUZZER 
def getBuzzer():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/3/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    respone_data=r.read().decode()
    respone_data=json.loads(respone_data)
    field3 = respone_data['field3']
    return field3
# HAM DOC TRANG THAI LED 
def getLed():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/4/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    respone_data=r.read().decode()
    respone_data=json.loads(respone_data)
    field4 = respone_data['field4']
    return field4
#HAM DOC TRANG THAI RELAY 

def getRelay():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/5/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data=json.loads(respone_data)
    pr
    field5 = respone_data['field5']
    return field5
# HAM DOC TRANG THAI NUT AUTO - MANUAL

def getMode():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/6/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data=json.loads(respone_data)
    field6 = respone_data['field6']
    return field6

while True:

    # HUMI = float(getHumi)
    # temp = getTEMP()
    # if(type(temp) is str):
    #     print(temp)
    #     temp = float(temp)
    #     print(temp)
    #     print(type(temp))
    # humi = getHumi()
    # if(type(humi) is str):
    #     print(humi)
    #     humi = float(humi)
    #     print(humi)
    #     print(type(humi))
    # mode = getMode()
    # if(type(mode) is str):
    #     print(mode)
    #     mode = float(mode)
    #     print(mode)
    #     print(type(mode))
    # buzzer = getBuzzer()
    # if(type(buzzer) is str):
    #     print(buzzer)
    #     buzzer = float(buzzer)
    #     print(buzzer)
    #     print(type(buzzer))
    # if mode == 1:
    # {'created_at': '2024-09-09T15:37:45Z', 'entry_id': 7, 'field2': '0.0'}
    # key-value

    req=request.Request("https://api.thingspeak.com/channels/%s/fields/2/x.json?api_key=%s"%(channelID,apiKeyRead),method="GET")
    r = request.urlopen(req)
    print(r.read())
    respone_data=r.read().decode()
    respone_data=json.loads(respone_data)
    print(respone_data)
    field2 = respone_data['field2']
    print(field2)

    time.sleep(1)