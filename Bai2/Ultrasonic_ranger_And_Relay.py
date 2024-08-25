from time import sleep
from grove.grove_relay import GroveRelay
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

sensor = GroveUltrasonicRanger(5)

relay = GroveRelay(16)

while True:
    distance = sensor.get_distance()
    print('{} cm'.format(distance))
    
    if distance < 20:
        relay.on()
        print('Relay On')
    else:
        relay.off()
        print('Relay Off')
    
    sleep(1)
    