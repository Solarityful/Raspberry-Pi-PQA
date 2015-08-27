#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

# Assign GPIO based on Headers LED down left side, Switches right 

LedPin_0 = 11
LedPin_1 = 15
LedPin_2 = 19
LedPin_3 = 21
LedPin_4 = 23
LedPin_5 = 29
LedPin_6 = 31
LedPin_7 = 33

SwitchPin_0 = 12
SwitchPin_1 = 16
SwitchPin_2 = 18
SwitchPin_3 = 22
SwitchPin_4 = 32
SwitchPin_5 = 36
SwitchPin_6 = 38
SwitchPin_7 = 40

# Move these into an array for future programming

LedArray = [LedPin_0, LedPin_1, LedPin_2, LedPin_3, LedPin_4, LedPin_5, LedPin_6, LedPin_7]
SwitchArray = [SwitchPin_0, SwitchPin_1, SwitchPin_2, SwitchPin_3, SwitchPin_4, SwitchPin_5, SwitchPin_6, SwitchPin_7]

PowerPin = 7
ResetValuePin = 35
AdderPin = 37


# Set the program to use Header GPIO format (pg 14 of Sunfounder book)

GPIO.setmode(GPIO.BOARD)

# Set each GPIO for LEDs as outputs 

GPIO.setup(LedPin_0, GPIO.OUT)
GPIO.setup(LedPin_1, GPIO.OUT)
GPIO.setup(LedPin_2, GPIO.OUT)
GPIO.setup(LedPin_3, GPIO.OUT)
GPIO.setup(LedPin_4, GPIO.OUT)
GPIO.setup(LedPin_5, GPIO.OUT)
GPIO.setup(LedPin_6, GPIO.OUT)
GPIO.setup(LedPin_7, GPIO.OUT)

# Set each GPIO for switches as inputs

GPIO.setup(SwitchPin_0, GPIO.IN)
GPIO.setup(SwitchPin_1, GPIO.IN)
GPIO.setup(SwitchPin_2, GPIO.IN)
GPIO.setup(SwitchPin_3, GPIO.IN)
GPIO.setup(SwitchPin_4, GPIO.IN)
GPIO.setup(SwitchPin_5, GPIO.IN)
GPIO.setup(SwitchPin_6, GPIO.IN)
GPIO.setup(SwitchPin_7, GPIO.IN)


GPIO.setup(PowerPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ResetValuePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(AdderPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Add event detections for GPIO

GPIO.add_event_detect(PowerPin, GPIO.FALLING)
GPIO.add_event_detect(ResetValuePin, GPIO.FALLING)
GPIO.add_event_detect(AdderPin, GPIO.FALLING)

# Initialize values

Currentbitvalue = 0
Storedbitvalue = 0 
Displayedbitvalue = 0
Bitarray = [0]*8

# Functions

def switchUp(switchnumber):
	return GPIO.input(switchnumber) == GPIO.HIGH

def lightOn(lednumber):
	GPIO.output(lednumber, GPIO.HIGH)
	
def lightOff(lednumber):
	GPIO.output(lednumber, GPIO.LOW)
	
def calculateCurrentBitValue(array):
	eightbitsum = 0
	for t in range(0,8):
		eightbitsum += array[t]*(2**t)
		
	return eightbitsum
	 
def resetValuesIfResetPressed():
	global Storedbitvalue
	global Displayedbitvalue
	
	if GPIO.event_detected(ResetValuePin):
		Storedbitvalue = 0
		Displayedbitvalue = 0

def powerSwitchCheck():
	if GPIO.event_detected(PowerPin):
		print 'Edge detected, SB = True, shutdown commencing'
		os.system("sudo shutdown -h now")

def computeAndLedHandler():
	for i in range(0, 8):
			
		if switchUp(SwitchArray[i]):
			print "Switch "+str(i)+" Pressed"
			lightOn(LedArray[i])
			Bitarray[i] = 1
			print "Led "+str(i)+" On..."
		else:
			
			lightOff(LedArray[i])
			Bitarray[i] = 0
			print "Led "+str(i)+" Off..."

def updateValues():
	global Currentbitvalue
	global Displayedbitvalue
	
	Currentbitvalue = calculateCurrentBitValue(Bitarray)
	Displayedbitvalue = Currentbitvalue	
	
def addToCurrentValue():
	global Storedbitvalue
	global Displayedbitvalue
	global Currentbitvalue
	
	if GPIO.event_detected(AdderPin):
		Storedbitvalue = Currentbitvalue + Storedbitvalue
		Displayedbitvalue = Storedbitvalue
		
	else:
		Displayedbitvalue = Storedbitvalue
	
def ledHandler():
	global Currentbitvalue
	global Storedbitvalue
	global Displayedbitvalue
	
	if Currentbitvalue != 0:
		Displayedbitvalue = Currentbitvalue
		print "Cur: ", str(Currentbitvalue)
		print "Stor: ", str(Storedbitvalue)
		print "Disp: ", str(Displayedbitvalue)
	
	else:
		print "Cur: ", str(Currentbitvalue)
		print "Stor: ", str(Storedbitvalue)
		print "Disp: ", str(Displayedbitvalue)

def keyboardCleanup():
	
	GPIO.output(LedPin_0, GPIO.LOW)
	GPIO.output(LedPin_1, GPIO.LOW)
	GPIO.output(LedPin_2, GPIO.LOW)
	GPIO.output(LedPin_3, GPIO.LOW)
	GPIO.output(LedPin_4, GPIO.LOW)
	GPIO.output(LedPin_5, GPIO.LOW)
	GPIO.output(LedPin_6, GPIO.LOW)
	GPIO.output(LedPin_7, GPIO.LOW)
	
	GPIO.cleanup()	

# Main program loop sleep set in seconds
try:
	while True:
		
		powerSwitchCheck()
		
		computeAndLedHandler()
		
		updateValues()
		
		resetValuesIfResetPressed()
		
		addToCurrentValue()
			
		ledHandler()
						
		time.sleep(.5)

except KeyboardInterrupt:
	
	keyboardCleanup()




