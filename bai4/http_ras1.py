from time import sleep
from urllib import request, parse
import random
from seeed_dht import DHT
sensor = DHT('11',5)

def PST_HTTP(temp, humi, data_random):
    url = f"https://api.thingspeak.com/update?api_key=VHNFT2CG8BJ0RP2O&field1={humi}&field2={temp}&field3={data_random}"
    request.urlopen(url)

while True:
    HUMI,TEMP =  sensor.read()
    data_random = random.randint(0,100)

    PST_HTTP(TEMP, HUMI, data_random)
    sleep(20)