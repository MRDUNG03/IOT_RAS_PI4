import paho.mqtt.client as mqtt
from gpiozero import LED, Buzzer
from grove.grove_relay import GroveRelay
import time
import datetime
import json

# Initialize GPIO devices
led = LED(24)
buzzer = Buzzer(16)
relay = GroveRelay(26)

# MQTT settings
broker = "mqtt.thingspeak.com"
port = 1883
channelID = "2643589"
apiKeyRead = "0FICQRIHXPHRENQB"
clientID = "mqtt_client"

# MQTT topics
topic_humi = f"channels/{channelID}/fields/1"
topic_temp = f"channels/{channelID}/fields/2"
topic_buzzer = f"channels/{channelID}/fields/3"
topic_led = f"channels/{channelID}/fields/4"
topic_relay = f"channels/{channelID}/fields/5"
topic_mode = f"channels/{channelID}/fields/6"

# Global variables to store data
humi = None
temp = None
buzzer_value = None
led_value = None
relay_value = None
mode = None

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global humi, temp, buzzer_value, led_value, relay_value, mode
    payload = msg.payload.decode("utf-8")

    if msg.topic == topic_humi:
        humi = payload
        print(f"Humidity: {humi}")
    elif msg.topic == topic_temp:
        temp = payload
        print(f"Temperature: {temp}")
    elif msg.topic == topic_buzzer:
        buzzer_value = payload
        print(f"Buzzer: {buzzer_value}")
    elif msg.topic == topic_led:
        led_value = payload
        print(f"LED: {led_value}")
    elif msg.topic == topic_relay:
        relay_value = payload
        print(f"Relay: {relay_value}")
    elif msg.topic == topic_mode:
        mode = payload
        print(f"Mode: {mode}")

# Setup MQTT Client
client = mqtt.Client(clientID)
client.on_message = on_message

client.username_pw_set(username="mqtt_client", password=apiKeyRead)
client.connect(broker, port, 60)

# Subscribe to the required topics
client.subscribe(topic_humi)
client.subscribe(topic_temp)
client.subscribe(topic_buzzer)
client.subscribe(topic_led)
client.subscribe(topic_relay)
client.subscribe(topic_mode)

# Start the loop to process MQTT messages
client.loop_start()

# Main control loop
while True:
    try:
        t = datetime.datetime.now().hour
        
        if mode and int(mode) == 1:  # Auto Mode
            print("Auto mode")
            print(t)
            if temp and int(temp) > 35:
                led.on()
                print("LED on")
            elif temp and int(temp) < 31:
                led.off()
                print("LED off")

            if humi and int(humi) > 90:
                relay.on()
                print("Relay on")
            elif humi and int(humi) < 60:
                relay.off()
                print("Relay off")

        elif mode and int(mode) == 0:  # Manual Mode
            print("Manual mode")
            if led_value and int(led_value) == 1:
                led.on()
                print("LED on")
            elif led_value and int(led_value) == 0:
                led.off()
                print("LED off")

            if relay_value and int(relay_value) == 1:
                relay.on()
                print("Relay on")
            elif relay_value and int(relay_value) == 0:
                relay.off()
                print("Relay off")

        time.sleep(20)

    except Exception as e:
        print(f"DISCONNECT: {e}")
        time.sleep(2)

# Stop the MQTT loop when done
client.loop_stop()
client.disconnect()
