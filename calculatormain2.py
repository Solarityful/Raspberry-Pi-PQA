#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

# Assign GPIO numbers based on Header column,
# (page 14 of Sunfounder manual) corresponds to physical position on BCM 
# www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python
# used the above link for lcd script, could improved

LCD_RS = 15
LCD_E = 19
LCD_D4 = 21
LCD_D5 = 23
LCD_D6 = 29
LCD_D7 = 31

SwitchPin_0 = 12
SwitchPin_1 = 16
SwitchPin_2 = 18
SwitchPin_3 = 22
SwitchPin_4 = 32
SwitchPin_5 = 36
SwitchPin_6 = 38
SwitchPin_7 = 40

# Define some device constants
LCD_WIDTH = 16 # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0XC0

E_PULSE = 0.0005
E_DELAY = 0.0005

# Move SwitchPin numbers into an array for future programming

SwitchArray = [SwitchPin_0, SwitchPin_1, SwitchPin_2, SwitchPin_3, SwitchPin_4, SwitchPin_5, SwitchPin_6, SwitchPin_7]

PowerPin = 7
ResetValuePin = 35
AdderPin = 37

# Set the program to use Header GPIO format (pg 14 of Sunfounder book)

GPIO.setmode(GPIO.BOARD)

# Set each GPIO for switches as inputs

GPIO.setup(SwitchPin_0, GPIO.IN)
GPIO.setup(SwitchPin_1, GPIO.IN)
GPIO.setup(SwitchPin_2, GPIO.IN)
GPIO.setup(SwitchPin_3, GPIO.IN)
GPIO.setup(SwitchPin_4, GPIO.IN)
GPIO.setup(SwitchPin_5, GPIO.IN)
GPIO.setup(SwitchPin_6, GPIO.IN)
GPIO.setup(SwitchPin_7, GPIO.IN)

# Set the GPIO for LEDs

GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

# Pi comes with internal pull-up and pull-down resistors, assign them
# here, can also do physical pull-up and pull-down resistors on board

GPIO.setup(PowerPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ResetValuePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(AdderPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Initialize values

Currentbitvalue = 0 # the value based on 8bit switch input
Storedbitvalue = 0 # the running sum stored on calculator

# used for earlier implementation, now pi has 2 lines for display,
# top row is storedbitvalue and bottom row is currentbitvalue
Displayedbitvalue = 0 

# Keeps track of what the user has switched on in 8bit array
Bitarray = [0]*8

# Functions

def switchUp(switchnumber):
	return GPIO.input(switchnumber) == GPIO.HIGH
	
def calculateCurrentBitValue(array):
	eightbitsum = 0
	for t in range(0,8):
		eightbitsum += array[t]*(2**t)
		
	return eightbitsum
	 
def resetValuesIfResetPressed(resetpin): 
	global Storedbitvalue
	global Displayedbitvalue
	
	Storedbitvalue = 0
	Displayedbitvalue = 0

def powerSwitchCheck(powerpin):
	print 'Edge detected, SB = True, shutdown commencing'
	lcd_string("Raspberry Pi",LCD_LINE_1)
	lcd_string("has shutdown",LCD_LINE_2)
	time.sleep(3)
	os.system("sudo shutdown -h now")

def computeAndLedHandler():
	for i in range(0, 8):
			
		if switchUp(SwitchArray[i]):
			print "Switch "+str(i)+" Pressed"
			Bitarray[i] = 1
		else:			
			Bitarray[i] = 0

# updates the values based on user input
def updateValues():
	global Currentbitvalue
	global Displayedbitvalue
	global Storedbitvalue
	
	Currentbitvalue = calculateCurrentBitValue(Bitarray)
	
	if Currentbitvalue != 0:
		Displayedbitvalue = Currentbitvalue	
	
	else:
		Displayedbitvalue = Storedbitvalue
		
# adds the current user input to the stored value		
def addToCurrentValue(addpin):
	global Storedbitvalue
	global Displayedbitvalue
	global Currentbitvalue
	
	Storedbitvalue = Currentbitvalue + Storedbitvalue
	Displayedbitvalue = Storedbitvalue
		
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)	

# prints to terminal and also changes message of lcd
def ledHandler():
	global Currentbitvalue
	global Storedbitvalue
	global Displayedbitvalue
	
	StringCurrentbitvalue = str(Currentbitvalue)
	StringStoredbitvalue = str(Storedbitvalue)
	StringDisplayedbitvalue = str(Displayedbitvalue)
	
	print "Cur: ", StringCurrentbitvalue
	print "Stor: ", StringStoredbitvalue
	print "Disp: ", StringDisplayedbitvalue
	
	lcd_string(StringCurrentbitvalue, LCD_LINE_2)
	lcd_string(StringStoredbitvalue, LCD_LINE_1)
	
def keyboardCleanup():
	
	GPIO.cleanup()	
    
# Add event detections for GPIO, triggers on button press, callback
# is provided but not necessary/used

GPIO.add_event_detect(PowerPin, GPIO.FALLING, callback = powerSwitchCheck, bouncetime = 300)
GPIO.add_event_detect(ResetValuePin, GPIO.FALLING, callback = resetValuesIfResetPressed, bouncetime = 300)
GPIO.add_event_detect(AdderPin, GPIO.RISING, callback = addToCurrentValue, bouncetime = 300)

#initliaze the LCD

lcd_init()

try:
	while True:
		
		computeAndLedHandler()
		
		updateValues()
			
		ledHandler()
		
		time.sleep(.1)

except KeyboardInterrupt:
	time.sleep(2)
	lcd_string("Program OFF",LCD_LINE_1)
	lcd_string("sudo python",LCD_LINE_2)
	keyboardCleanup()





