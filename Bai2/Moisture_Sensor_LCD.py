#from LCD import setText
#from LCD import setText_norefresh
from grove.display.jhd1802 import JHD1802
from time import sleep
from grove.gpio import GPIO
from grove.grove_moisture_sensor import GroveMoistureSensor

ms_pin = 0
lcd = JHD1802()

sensor = GroveMoistureSensor(ms_pin)

while True:
    mois = sensor.moisture
    if 0 <= mois and mois < 300:
        level = 'dry'
    elif 300 <= mois and mois < 600:
        level = 'moist'
    else:
        level = 'wet'
    
    print("Moisture: {}, {}".format(mois, level))
    lcd.setCursor(0, 0)
    lcd.write("Moisture: {0:>6}".format(mois))
    lcd.setCursor(1, 0)
    lcd.write("{0:>16}".format(level))
    sleep(1)
        
    