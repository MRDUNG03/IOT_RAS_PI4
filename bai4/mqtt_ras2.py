import paho.mqtt.client as mqtt
import json
from time import sleep
from gpiozero import LED
from gpiozero import Buzzer
from urllib import request, parse
from grove.grove_relay import GroveRelay
from grove.display.jhd1802 import JHD1802

LED = LED(18)
BUZZER = Buzzer(22)
RELAY = GroveRelay(16)
LCD = JHD1802()

def on_connect(client, userdata, flags, rc):
    print("Connected with results code {}".format(rc))
    channel_ID = "2638952"
    client.subscribe("channels/%s/subscribe" % channel_ID)

def on_disconnect(client, userdata, rc):
    print("disconnect from broker")
    
def on_message(client, userdata, message):
    data_fields = message.payload.decode()
    data_fields = json.loads(data_fields)

    LIGHT = int(data_fields["field3"])
    HUMI = int(data_fields["field1"])
    TEMP = int(data_fields["field2"])

    print("lcd: \nNhiet do: %s - Do am: %s - Rand: %s" %(TEMP,HUMI,LIGHT))
    LCD.clear()
    LCD.setCursor(0,0)
    LCD.write('TEMP:{}'.format(TEMP))
    LCD.setCursor(0,8)
    LCD.write('HUM:{}'.format(HUMI))
    LCD.setCursor(1,0)
    LCD.write('RAND: {}'.format(LIGHT))

    if LIGHT > 50:
        LED.on()             
    elif LIGHT < 50:
        LED.off()
    
    if TEMP > 37:
        BUZZER.beep(1)
    elif TEMP < 31:
        BUZZER.beep(0)
    
    if HUMI > 90:
        RELAY.on()
    elif HUMI < 60:
        RELAY.off()

client_id = 'IhI1OyccJDEmIRwKHy04Kzo'
client = mqtt.Client(client_id)
# gan cac chuong trinh con
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username='IhI1OyccJDEmIRwKHy04Kzo', password= 'NONYmBz3FrH9o3hyCoYGojeN')
client.connect("mqtt3.thingspeak.com", 1883,68)
client.loop_forever()