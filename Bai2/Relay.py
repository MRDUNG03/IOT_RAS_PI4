from time import sleep
from grove.gpio import GPIO
import sys

relay_pin = 12

class GroveRelay(GPIO):
    def __init__(self, pin):
        super(GroveRelay, self).__init__(pin, GPIO.OUT)
    
    def on(self):
        self.write(1)
        
    def off(self):
        self.write(0)
        
relay = GroveRelay(relay_pin)

while True:
    try:
        relay.on()
        sleep(1)
        relay.off()
        sleep(1)
    except KeyboardInterrupt:
        relay.off()
        print("Exit")
        exit(1)