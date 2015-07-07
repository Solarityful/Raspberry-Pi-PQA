#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LedPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LedPin, GPIO.OUT)

try:
	while True:
		print 'Led On...'
		GPIO.output(LedPin, GPIO.LOW)
		time.sleep(0.5)
		print '...Led Off'
		GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(0.5)
except KeyboardInterrupt:
	GPIO.output(LedPin, GPIO.LOW)
	GPIO.cleanup()

#testing git commit feature
