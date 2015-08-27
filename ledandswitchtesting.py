#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LedPin = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(LedPin, GPIO.OUT)

try:
	while True:
		GPIO.output(LedPin, GPIO.HIGH)
		
except KeyboardInterrupt:
	GPIO.output(LedPin, GPIO.LOW)
	GPIO.cleanup()
