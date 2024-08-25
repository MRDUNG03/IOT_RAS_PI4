from time import time
start_time = time()
from time import sleep
import sys
import math
from grove.adc import ADC
from grove.gpio import GPIO
#from grove.display.jhd1802 import JHD1802
from grove.grove_ryb_led_button import GroveLedButton
from grove.button import Button
from numpy import interp
import RPi.GPIO as IO
from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
from grove.grove_relay import GroveRelay
from grove.grove_moisture_sensor import GroveMoistureSensor
from seeed_dht import DHT
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

#Grove - 16x2 LCD connected to I2C port
'''
lcd = JHD1802()
lcd.clear()
lcd.setCursor(0,0)
lcd.write("Created by N5")
lcd.setCursor(0,1)
lcd.write("Developed by NN")
sleep(10)
lcd.clear()
'''
#--------------------------------------
#RED LED Button connected to D5 port (GPIO 5)
button = GroveLedButton(5)
click_count = 1
#--------------------------------------
#Pin port
digital_pin = 16
analog_pin = 0
pwm_pin = 12
#--------------------------------------
#Flag active
'''
buzzer_active = False
relay_active = False
servo_active = False
mnPirMS_active = False
moisture_sensor_active = False
light_sensor_active = False
dht_sensor_active = False
ultrasonic_ranger_active = False
adc_sensor_active = False
'''
#Reset State
def reset_state():
    '''
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write("Test Grove!")
    lcd.setCursor(0,1)
    '''
    print("Test Grove!")
    '''
    lcd.write("Loading... (5s)")
    sleep(1)
    lcd.write("Loading... (4s)")
    sleep(1)
    '''
    '''
    lcd.write("Loading... (3s)")
    sleep(1)
    lcd.write("Loading... (2s)")
    sleep(1)
    lcd.write("Loading... (1s)")
    '''
    sleep(1)
    click_count = 1
    '''
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write("Click 2 Change")
    lcd.setCursor(0,1)
    lcd.write("Press 2 select")
    '''
def on_event(index, event, tm):
    if event & Button.EV_SINGLE_CLICK:
        if (0 < click_count) and (click_count < 10):
            click_count =+ 1
        else:
            click_count = 1
        print("Click count: {}".format(click_count))
        
    elif event & Button.EV_DOUBLE_CLICK:
        reset_state()
        
    elif event & Button.EV_LONG_PRESS:
        if click_count == 1:
            print("Test Buzzer!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at PWM')
            sleep(2)
            #buzzer_active = True
            '''
            buzzer_test()
        elif click_count == 2:
            print("Test Relay!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at D16')
            sleep(2)
            #relay_active = True
            '''
            relay_test()
        elif click_count == 3:
            print("Test Servo!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at PWM')
            sleep(2)
            #servo_active = True
            '''
            servo_test()
        elif click_count == 4:
            print("Test Motion Sensor!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at D16')
            sleep(2)
            #mnPirMS_active = True
            '''
            mnPirMS()
        elif click_count == 5:
            print("Test Moisture Sensor!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at A0')
            sleep(2)
            #moisture_sensor_active = True
            '''
            moisture_sensor_test()
        elif click_count == 6:
            print("Test Light Sensor!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at A0')
            sleep(2)
            #light_sensor_active = True
            '''
            light_sensor_test()
        elif click_count == 7:
            print("Test DHT Sensor!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at D16')
            sleep(2)
            #dht_sensor_active = True
            '''
            dht_sensor_test()
        elif click_count == 8:
            print("Test Ultrasonic Ranger!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at D16')
            sleep(2)
            #ultrasonic_ranger_active = True
            '''
            ultrasonic_ranger_test()
        elif click_count == 9:
            print("Test ADC Sensor!")
            '''
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.write('Connect at A0')
            sleep(2)
            #adc_sensor_active = True
            '''
            adc_sensor_test()
        reset_state()
def buzzer_test():
    if buzzer_active:
        notes = {
            "Do": 261.63,
            "Re": 293.66,
            "Mi": 329.63,
            "Fa": 349.23,
            "Sol": 392,
            "La": 440,
            "Si": 493.88,
            "Do2": 523.25
        }
        buzzer = GPIO(pwm_pin, GPIO.OUT)
        for note in notes:
            duration = 0.5
            frequency = notes[note]
            periol = 1.0 / frequency #periol la chu ky (T) = 1/f
            delay = periol / 2 #Tgian ma chan GPIO duoc bat/tat, no bang (1/2).T de tao ra song vuong, mo phong song am
            cycles = int(duration * frequency)
            for _ in range(cycles):
                buzzer.write(1)
                sleep(delay)
                buzzer.write(0)
                sleep(delay)
            sleep(0.1)
        buzzer.write(0)
    #reset_state()

#--------------------------------
def relay_test():
    '''
    class GroveRelay(GPIO):
        def __init__(self, pin):
            super(GroveRelay, self).__init__(pin, GPIO.OUT)
        
        def on(self):
            self.write(1)
            
        def off(self):
            self.write(0)
    '''
    relay = GroveRelay(digital_pin)
    relay.on()
    sleep(0.6)
    relay.off()
    sleep(0.6)
    relay.on()
    sleep(0.6)
    relay.off()
    sleep(0.6)
    #reset_state()
    
#--------------------------------
    
def servo_test():
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    class GroveServo:
        MIN_DEGREE = 0
        MAX_DEGREE = 180
        INIT_DUTY = 2.5
        
        def __init__(self, channel):
            IO.setup(channel, IO.OUT)
            self.pwm = IO.PWM(channel, 50)
            self.pwm.start(GroveServo.INIT_DUTY)
            
        def __del__(self):
            self.pwm.stop()
        
        def setAngle(self, angle):
            angle = max(min(angle, GroveServo.MAX_DEGREE), GroveServo.MIN_DEGREE)
            tmp = interp(angle, [0,180], [25, 125])
            self.pwm.ChangeDutyCycle(round(tmp/10.0,1))
            
    servo = GroveServo(pwm_pin)
    for x in range(0, 180, 10):
        print(x, "degree")
        servo.setAngle(x)
        sleep(0.1)
    
    for x in range(180, 0, -10):
        print(x, "degree")
        servo.setAngle(x)
        sleep(0.1)
        
    #reset_state()

#------------------------------------
def mnPirMS_test():
    def on_detect():
        print('Motion Detected!')
        button.led.light(True)
        sleep(1)
        button.led.light(False)
        
    sensor.on_detect = on_detect
    #reset_state()
#----------------------------------
def moisture_sensor_test():
    sensor = GroveMoistureSensor(analog_pin)
    mois = sensor.moisture
    level = 'NaN'
    def checklv():
        if 0 <= mois and mois < 300:
            level = 'dry'
        elif 300 <= mois and mois < 600:
            level = 'moist'
        else:
            level = 'wet'
    
    for i in range(0,3):
        mois = sensor.moisture
        checklv()
        print("Moisture: {}, {}".format(mois, level))
        '''
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.write("Moisture: {0:>6}".format(mois))
        lcd.setCursor(1, 0)
        lcd.write("{0:>16}".format(level))
        '''
        sleep(1.5)

#-----------------------------
def light_sensor_test():
    class GroveLigthSensor:
        def __init__(self, channel):
            self.channel = channel
            self. adc = ADC()
            
        @property
        def light(self):
            value = self.adc.read(self.channel)
            return value
    sensor = GroveLigthSensor(analog_pin)
    print('Detecting Light...')
    for i in range(0,3):
        print('Light value: {0}'.format(sensor.light))
        '''
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.write("Light: {0}".format(sensor.light))
        '''
        sleep(1.5)
        
#------------------------------
def dht_sensor_test():
    sensor = DHT('11', digital_pin)
    hum, tem = sensor.read()
    print("Temperature {}C, humidity {}%".format(tem, hum))
    '''
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write("T: {0:2}C".format(tem))
    lcd.setCursor(0,0)
    lcd.write("H: {0:5}%".format(hum))
    '''
    sleep(3)
    
#------------------------------
def ultrasonic_ranger_test():
    sensor = GroveUltrasonicRanger(digital_pin)
    for i in range(0,5):
        distance = sensor.get_distance()
        print('{} cm'.format(distance))
        '''
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.write('{} cm'.format(distance))
        '''
        
#-----------------------------------------
def adc_sensor_test():
    for i in range(0,10):        
        sensor = ADC(analog_pin)
        value = sensor.read_voltage(0) # Ket qua 0 - 3299 (mV)
        #value = sensor.read_raw(0)    # Ket qua dang 12 bit tu 0 - 4095
        #value = sensor.read(0)        # Ket qua ti le dien ap do chia 0.1% (0 - 999)
        print(value)
        '''
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.write(value)
        '''
        sleep(2)
    
    
#Initial Screen Initialization
reset_state()
#Wait button event
button.on_event = on_event

while True:
    elapsed_time = time() - start_time
    print(elapsed_time)
    sleep(1)