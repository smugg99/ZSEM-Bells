#!/usr/bin/env python3

import OPi.GPIO as GPIO
from time import sleep

pin: int = 11
GPIO.setboard(GPIO.H616)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)
sleep(1)
while True:
    GPIO.output(pin, GPIO.LOW)
    sleep(1)
    GPIO.output(pin, GPIO.HIGH)