from time import sleep
import sys

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

DISPLAY_TEXT_ADDR = 0x3e #Dia chi cua LCD I2C

def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)

def setText(text):
    textCommand(0x01) # clear display
    sleep(0.05)
    textCommand(0x08 | 0x04) #display on, no cursor
    textCommand(0x28)
    sleep(0.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40, ord(c))
        
def setText_norefresh(text):
    textCommand(0x02)
    sleep(0.05)
    textCommand(0x08 | 0x04)
    textCommand(0x28)
    sleep(0.05)
    count = 0
    row = 0
    while len(text) < 32:
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))
'''        
setText("Hello World!\nThis is an LCD test")
sleep(2)
for c in range(0,255):
    setText_norefresh("Going to sleep in {}...".format(str(c)))
    sleep(0.1)
setText("Bye bye, this should wrap onto next line")
'''