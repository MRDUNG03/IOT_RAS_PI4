from time import sleep
from grove.adc import ADC

sensor = ADC(0)

while True:
    value = sensor.read_voltage(0) # Ket qua 0 - 3299 (mV)
    #value = sensor.read_raw(0)    # Ket qua dang 12 bit tu 0 - 4095
    #value = sensor.read(0)        # Ket qua ti le dien ap do chia 0.1% (0 - 999)
    print(value)
    sleep(2)