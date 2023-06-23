#!/usr/bin/env python3

import OPi.GPIO as GPIO
from time import sleep

pin: int = 12
GPIO.setboard(GPIO.H616)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(pin, GPIO.HIGH)
sleep(4)
while True:
    GPIO.output(pin, GPIO.LOW)
    print(GPIO.input(pin))
    sleep(4)
    GPIO.output(pin, GPIO.HIGH)
    print(GPIO.input(pin))