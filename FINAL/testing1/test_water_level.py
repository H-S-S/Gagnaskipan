import RPi.GPIO as GPIO
import os
from time import sleep

SEN = 21


GPIO.setmode(GPIO.BCM)
GPIO.setup(SEN, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

while True:
    if GPIO.input(SEN) == False:
        print('no water')
    else:
        print('there is water')
    sleep(1)