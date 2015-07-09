#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)

ResetValuePin = 35
AdderPin = 37

GPIO.setup(ResetValuePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(AdderPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.add_event_detect(ResetValuePin, GPIO.FALLING)
GPIO.add_event_detect(AdderPin, GPIO.FALLING)

try:
	while True:
		if GPIO.event_detected(ResetValuePin):
			print "Reset works!"
			
		if GPIO.event_detected(AdderPin):
			print "Adder works!"
			
except KeyboardInterrupt:
	GPIO.cleanup()
