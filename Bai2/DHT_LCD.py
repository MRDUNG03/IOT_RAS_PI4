from time import sleep
from seeed_dht import DHT
#from grove.display.jhd1802 import JHD1802

#lcd = JHD1802()

sensor = DHT('11', 5)
while True:
    hum, tem = sensor.read()
    print("Temperature {}C, humidity {}%".format(tem, hum))
    #lcd.setCursor(0,0)
    #lcd.write("T: {0:2}C".format(tem))
    #lcd.setCursor(0,0)
    #lcd.write("H: {0:5}%".format(hum))
    sleep(1)
    