#!/usr/bin/env python3
from time import sleep
import OPi.GPIO as GPIO

def main():
    GPIO.setboard(GPIO.H616)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(12, GPIO.OUT, GPIO.HIGH)

    while True:
        sleep(1)
        GPIO.output(12, GPIO.LOW)
        print("Relay on")

        sleep(1)
        GPIO.output(12, GPIO.HIGH)
        print("Relay off")


if __name__ == "__main__":
    main()
