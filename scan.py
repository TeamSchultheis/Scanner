#!/usr/bin/env python

'''
This is the main python script for the TW (Raspberry) Pi Scanner project.
It is currently functional using the Raspberry Pi 1.

The stepper motor currently in use has 200 steps. Thus with 5 increments of 40 steps, we can complete a full revolution
and obtain five different images.

Hardware Setup:
RPi
A9488 Stepper Driver
5V regulator
6mm Tactile Switch

________________________Pi Connections________________________
5V - 5V
GND - GND
3.3V - switch terminal 1
GPIO 24 - switch terminal 2, parallel with 10k --> GND
GPIO 23 - A9488 breakout STEP
GPIO 18 - A9488 breakout DIR
______________________________________________________________



______________________A9488 Connections_______________________
VDD - RPi 3.3V
GND - GND
VMOT - 12V from raw supply
A9488 SLP - A9488 RST
STEP - RPi 23
DIR - RPi 18
______________________________________________________________



___________________5V Regulator Connections___________________
VIN - 12V from raw supply
GND - GND
VOUT - 5V
______________________________________________________________

Dan Bogachek
10/1/15
'''



import time
import RPi.GPIO as GPIO
import sys
import os
import picamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
step = 23
dir = 18
button = 24
timestep = .001
run_times = 0

camera = picamera.PiCamera()


GPIO.setup(step, GPIO.OUT)
GPIO.setup(dir, GPIO.OUT)
GPIO.setup(button, GPIO.IN)

directory = sys.argv[1]
filename = sys.argv[1]

def clockwise(cycles):
	GPIO.output(dir, True)
	for i in range(0, cycles):
		GPIO.output(step, True)
		time.sleep(timestep)
		GPIO.output(step, False)
		time.sleep(timestep)

def counter(cycles):
	GPIO.output(dir, False)
	for i in range (0, cycles):
		GPIO.output(step, True)
		time.sleep(timestep)
		GPIO.output(step, False)
		time.sleep(timestep)

def advance(reps, steps, run_times):
	factor = run_times*5;
	for i in range(factor, reps+factor):
		clockwise(steps)
		time.sleep(.5)

		if(i<10): camera.capture('img000%d.jpg' % i)
		elif(i<100): camera.capture('img00%d.jpg' % i)
		elif(i<1000): camera.capture('img0%d.jpg' % i)
		else: camera.capture('img%d.jpg' % i)

		time.sleep(.5)

flag = 0
i = 1

os.chdir("/home/pi/Documents/piscanner/")

while flag is 0:
	if os.path.exists(directory):
		directory = sys.argv[1] + str(i)
	else:
		os.mkdir(directory)
		flag = 1

	i = i + 1

os.chdir(directory)


print directory

while 1:
	if GPIO.input(button):
		advance(5, 40, run_times)
		run_times = run_times + 1	

GPIO.cleanup()
