#!/usr/bin/env python3

import OPi.GPIO as GPIO
from time import sleep

pin: int = 26
GPIO.setboard(GPIO.H616)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin, GPIO.OUT)

while True:
    GPIO.output(pin, GPIO.LOW)
    sleep(1)
    GPIO.output(pin, GPIO.HIGH)