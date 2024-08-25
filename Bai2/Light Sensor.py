from time import sleep
import sys
import math
from grove.adc import ADC
#----------------------
sensor_pin = 0 #Channel A0

class GroveLigthSensor:
    def __init__(self, channel):
        self.channel = channel
        self. adc = ADC()
        
    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value

sensor = GroveLigthSensor(sensor_pin)

print('Detecting Light...')
while True:
    print('Light value: {0}'.format(sensor.light))
    sleep(1)