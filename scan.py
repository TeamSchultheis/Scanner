#!/usr/bin/env python

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
