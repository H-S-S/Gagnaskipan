import RPi.GPIO as GPIO
import os
from time import sleep

class WaterLevel():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def read(self):
        return GPIO.input(self.pin)


if __name__ == "__main__":
    SEN = 21

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SEN, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

    while True:
        if GPIO.input(SEN) == False:
            print('no water')
        else:
            print('there is water')
        sleep(1)