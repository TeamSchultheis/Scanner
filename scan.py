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
num_images = 20


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
	factor = run_times*num_images
	for i in range(factor, reps+factor):
		clockwise(steps)
		time.sleep(.01)

		if(i<10): camera.capture('img000%d.jpg' % i)
		elif(i<100): camera.capture('img00%d.jpg' % i)
		elif(i<1000): camera.capture('img0%d.jpg' % i)
		else: camera.capture('img%d.jpg' % i)

		time.sleep(.01)

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
		advance(num_images, 200/num_images, run_times)
		run_times = run_times + 1	

GPIO.cleanup()
