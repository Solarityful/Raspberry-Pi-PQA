#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os

# Assign GPIO based on Headers
LedPin = 11
ButtonPin = 12
PowerPin = 7

# Set the program to use Header GPIO format (pg 14 of Sunfounder book)
GPIO.setmode(GPIO.BOARD)

# Set each GPIO 
GPIO.setup(LedPin, GPIO.OUT)
GPIO.setup(ButtonPin, GPIO.IN)
GPIO.setup(PowerPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Add event detections for GPIO
GPIO.add_event_detect(PowerPin, GPIO.FALLING)

# Main program loop sleep set in seconds
try:
	while True:
		
		# If power button has been pressed, print a message and shutdown pi
		if GPIO.event_detected(PowerPin):
			print 'Edge detected, SB = True, shutdown commencing'
			os.system("sudo shutdown -h now")
		
		# Checks that the switch is not pressed, LED is off	
		if GPIO.input(ButtonPin) == GPIO.HIGH:
			# switch up
			print "button down"
			GPIO.output(LedPin, GPIO.HIGH)
			print 'Led On...'
		else:
			# switch down
			print "button up"
			GPIO.output(LedPin, GPIO.LOW)
			print 'Led Off...'
					
		time.sleep(.5)

except KeyboardInterrupt:
	GPIO.output(LedPin, GPIO.LOW)
	GPIO.cleanup()




