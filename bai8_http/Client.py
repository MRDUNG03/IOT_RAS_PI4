from urllib import request
from time import sleep
import json
from seeed_dht import DHT      
import datetime 
from gpiozero import LED

API_KEY = "nhom2_iot"
sensor = DHT('11', 5)
yd = 0
L1 = LED(18)
L2 = LED(24)
L3 = LED(26)
def make_params(humi,temp,led1, led2, led3,  yd):
    current_time = datetime.datetime.now()  
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S') 
    
    data = {
        "id": yd,
        "device": "RaspberryPi_4",
        "data1": humi,
        "data2": temp,
        "time": formatted_time,  
        "led1": led1,  
        "led2": led2,
        "led3": led3 
    }
    
    params = json.dumps(data).encode()  
    return params

def api_post(params):
    req = request.Request("http://192.168.1.134:9500/update_post", method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("accept", "application/json")
    req.add_header("api_key", API_KEY)  
    r = request.urlopen(req, data=params)
    response_data = r.read()
    return response_data

def api_get():
    req = request.Request("http://192.168.1.134:9500/get", method="GET")
    req.add_header("api_key", API_KEY) 
    r = request.urlopen(req)
    response_data = r.read().decode()
    response_data = json.loads(response_data)
    return response_data



while True:
    
    humi, temp = sensor.read()
    if humi != 0 or temp != 0:
        yd += 1
        if yd % 2 == 0:
            L1.on()
            L2.on()
            L3.off()
            led1_status = "1"
            led2_status = "1"
            led3_status = "0"
        if yd % 2 != 0:
            L1.on()
            L2.off()
            L3.on()
            led1_status = "1"
            led2_status = "0"
            led3_status = "1"
        params = make_params(humi,temp,led1_status,led2_status, led3_status , yd)
        print(params)
        print(api_post(params))  
        print("Reading sensor data...")
        print(api_get())  
        sleep(5)  