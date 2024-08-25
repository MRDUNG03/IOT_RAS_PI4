from time import sleep
from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
from grove.grove_relay import GroveRelay

sensor = GroveMiniPIRMotionSensor(5)

relay = GroveRelay(16)

def on_detect():
    print('Motion Detected!')
    relay.on()
    print('Relay on 2s')
    sleep(2)
    relay.off()
    print('Relay off')
    
sensor.on_detect = on_detect

while True:
    sleep(1)