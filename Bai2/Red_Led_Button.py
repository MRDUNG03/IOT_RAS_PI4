from grove.button import Button
from grove.grove_ryb_led_button import GroveLedButton
from time import sleep

button = GroveLedButton(5)

def on_envent(index, event, tm):
    if event & Button.EV_SINGLE_CLICK:
        print("Led On")
        button.led.light(True)
    elif event & Button.EV_LONG_PRESS:
        print("Led Off")

button.on_event = on_envent
while True:
    sleep(1)

