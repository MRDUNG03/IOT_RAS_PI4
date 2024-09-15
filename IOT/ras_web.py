import paho.mqtt.client as mqtt
from urllib import request, parse
from gpiozero import LED
from gpiozero import Buzzer
from grove.grove_relay import GroveRelay
import time
import datetime
import json

led = LED(24)
buzzer = Buzzer(16)
relay = GroveRelay(26)
apiKeyRead = "0FICQRIHXPHRENQB"
channelID = "2643589"
def getHumi():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/1/last.json?api_key=%s"%(channelID,apiKeyRead), method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    field1 = response_data.get('field1')
    print(field1)
    return field1
def getTemp():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/2/last.json?api_key=%s"%(channelID,apiKeyRead), method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    field2 = response_data.get('field2')  # Sử dụng get để tránh lỗi key nếu không có dữ liệu
    print(field2)
    return field2
def getBuzzer():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/3/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    value = response_data.get("field3")
    return value
def getLed():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/4/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    value = response_data.get("field4")
    return value
def getRelay():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/5/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    value = response_data.get("field5")
    return value

def getMode():
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/6/last.json?api_key=%s"% (channelID, apiKeyRead), method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    value = response_data.get("field6")
    return value






while True:
    try:
        humi = getHumi()
        temp = getTemp()
        mode = getMode()
        led_value = getLed()
        relay_value = getRelay()
        buzzer_value = getBuzzer()
        t = datetime.datetime.now().hour
        
        if int(mode) == 1:
            print("Chế độ auto")
            print(t)
            if 18 <= int(t) <= 22:  # 18h đến 22h
                led.on()
                print("Led bật")
                led_value = 1
            else:
                led.off()
                print("Led tắt")
                led_value = 0

            if int(temp) > 37:
                buzzer.beep(1)
                print("Loa bật")
                buzzer_value = 1
            elif int(temp) < 31:
                buzzer.beep(0)
                print("Loa tắt")
                buzzer_value = 0

            if int(humi) > 90:
                relay.on()
                print("Relay bật")
                relay_value = 1
            elif int(humi) < 60:
                relay.off()
                print("Relay tắt")
                relay_value = 0

            time.sleep(20)

        elif int(mode) == 0:
            print("Chế độ manual")
            if int(led_value) == 1:
                led.on()
            elif int(led_value) == 0:
                led.off()

            if int(buzzer_value) == 1:
                buzzer.beep(1)
                print("Loa bật")
            elif int(buzzer_value) == 0:
                buzzer.beep(0)
                print("Loa tắt")

            if int(relay_value) == 1:
                relay.on()
                print("Relay bật")
            elif int(relay_value) == 0:
                relay.off()
                print("Relay tắt")
    except:
        print("no connected")
        time.sleep(2)