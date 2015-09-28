#!/usr/bin/env python

'''

This code is for the TW Pi Scanner.

Given pulses of .01 seconds, this stepper motor has 200 steps, hence 40 steps advancement * 5 = full revolution.

Upon the user's press of the input button, the stage rotates and takes a picture for a total of 5 times
to complete a single revolution. The 5 images are saved in the directory provided and are named after said
directory.

GPIO 23 (step) on the Pi is the step control on the A9488 stepper driver
GPIO 18 (dir) on the Pi is the direction control on the A9488 stepper driver
GPIO 24 (button) on the Pi is the tactile switch input


Hardware Connections



//////////////////// 5V Regulator

VIN <--> VCC (12V and abvove)
GND <--> GND
VOUT <--> RPi 5V

////////////////////




//////////////////// RPi

step <--> A9488 STEP
dir <--> A9488 DIR
button <--> tactile switch output, parallel with 10K pull-down to GND
GND <--> GND
5V <--> VOUT
3.3V <--> A9488 VDD

////////////////////




//////////////////// A9488 Stepper Driver

IMPORTANT FOR HARDWARE SETUP: Current Limit = VREF × 2.5
Value set at .4V so that current limit is 1A
-
VMOT <--> VCC
GND <--> GND
VDD <--> VDD 3.3V from RPi - RPi IO is 3.3V and VDD on the stepper driver uses VDD as logic reference
GND <--> GND
-
Connect RST & SLP
STEP <--> RPi step
DIR <--> RPi dir
-
1A,1B - first stepper coil
2A,2B - second stepper coil

////////////////////




//////////////////// Tactile Switch

tactile switch input <--> 3.3V
tactile switch output <--> RPi button, parallel with 10k pull-down to GND

////////////////////



Dan Bogachek
09/28/2015

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
	for i in range(0+factor, reps+factor):
		clockwise(steps)
		time.sleep(.5)
		camera.capture('blah%d.jpg' % i)
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
