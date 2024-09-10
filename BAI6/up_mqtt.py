import paho.mqtt.client as mqtt
import json
from time import sleep
from urllib import request, parse
from grove.display.jhd1802 import JHD1802
from seeed_dht import DHT
# lcd=LCD()
dht = DHT("11",5)

def on_connect(client, userdata, flags, rc):
    print("Connected with results code {}".format(rc))
    channel_ID = ""
    client.subscribe("channels/%s/subscribe" % channel_ID)

def on_disconnect(client, userdata, rc):
    print("disconnect from broker")
    
def on_message(client, userdata, message):
    data_fields = message.payload.decode()
    data_fields = json.loads(data_fields)

 
    HUMI = int(data_fields["field1"])
    TEMP = int(data_fields["field2"])
   

    print("lcd: \nNhiet do: %s - Do am: %s - Rand: %s" %(TEMP,HUMI))
    # lcd.clear()
    # lcd.setCursor(0,0)
    # lcd.write('TEMP:{}'.format(TEMP))
    # lcd.setCursor(0,8)
    # lcd.write('HUM:{}'.format(HUMI))
    # lcd.setCursor(1,0)
   

    

client_id = ''
client = mqtt.Client(client_id)
# gan cac chuong trinh con
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username='', password= '')
client.connect("mqtt3.thingspeak.com", 1883,68)
client.loop_forever()