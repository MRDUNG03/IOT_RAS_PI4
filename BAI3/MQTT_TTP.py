import paho.mqtt.client as mqtt
from time import sleep        
from grove.grove_light_sensor_v1_2 import GroveLightSensor 
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger 
from grove.display.jhd1802 import JHD1802 
from seeed_dht import DHT 
from urllib import request, parse
#KHAI BAO CHAN MODULE WITH RASPI4
lcd = JHD1802()
sensor = DHT('11',5)
Distance = GroveUltrasonicRanger(12)
Light_led = GroveLightSensor(2)
#CONNETED MQTT
def connect():
    username = "DCESGRsrJxgGGTUdFyIUJCo"
    clientId = "DCESGRsrJxgGGTUdFyIUJCo"
    password = "GaLVhPqBCEv6zDwV1KxhApn8"
    client = mqtt.Client(clientId)
    client.username_pw_set(username=username, password=password)
    client.connect("mqtt3.thingspeak.com", 1883, 60)
    return client
def thingspeakMQTT(humi, temp, light, distance, client):
    channel_ID = "2633783"
    instr = f"&field1={humi}&field2={temp}&field3={light}&field4={distance}&status=MQTTPUBLISH"
    client.publish(f"channels/{channel_ID}/publish", instr)
    
def PST_HTTP(humi, temp, light, distance):
    url = f"https://api.thingspeak.com/update?api_key=RK84OE4D9FP7EJ3L&field1={humi}&field2={temp}&field3={light}&field4={distance}"
    request.urlopen(url)

mqtt_client = connect()
while 1:
    try:   
        HUMI,TEMP =  sensor.read()
        DISTANCE = int(Distance.get_distance())
        LIGHT = Light_led.light
        # in LEN LCD
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.write('{0:0.1f}C'.format(TEMP))
        lcd.setCursor(0,6)
        lcd.write('{0:0.1f}%'.format(HUMI))
        lcd.setCursor(1,0)
        lcd.write('{0:2}'.format(LIGHT))
        lcd.setCursor(1,6)        
        lcd.write('{0:2}Cm'.format(DISTANCE))
      
        #GUI DATA LEN MQTT_HTTP
        thingspeakMQTT(HUMI, TEMP, LIGHT, DISTANCE, mqtt_client)
        PST_HTTP(HUMI, TEMP, LIGHT, DISTANCE)
        sleep(20)
    except:
      print("NO CONNECT")
      sleep(2)
                        
    
    
    
    
    
    
    
