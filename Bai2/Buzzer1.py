from time import sleep
from grove.gpio import GPIO

#Khai báo chân GPIO điều khiển Buzzer
buzzer_pin = 12

#Tao 1 Dictionary chua cac note muon phat
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

buzzer = GPIO(buzzer_pin,GPIO.OUT)

def play_tone(buzzer, frequency, duration): #duration la tgian phat cua am thanh
    periol = 1.0 / frequency #periol la chu ky (T) = 1/f
    delay = periol / 2 #Tgian ma chan GPIO duoc bat/tat, no bang (1/2).T de tao ra song vuong, mo phong song am
    cycles = int(duration * frequency)
    for _ in range(cycles):
        buzzer.write(1)
        sleep(delay)
        buzzer.write(0)
        sleep(delay)
        
        
while True:
    for note in notes:
        play_tone(buzzer, notes[note], 0.5)
        sleep(0.1)
        
buzzer.write(0)
    