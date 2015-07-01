#!/usr/bin/python3
#
# Cycles colour of an RGB LED
#
# uses PWM outputs to adjust brightness of RGB components
# with hue smoothly changing from 0 to 1
#
#   v1.0    28/4/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import RPi.GPIO as GPIO
import colorsys
import time

# pin assignments
red = 23                    # red LED on GPIO 23 (active high)
green = 22                  # green LED on GPIO 22 (active high)
blue = 27                   # blue LED on GPIO 27 (active high)

# configure I/O
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# configure pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# setup PWM outputs
pr = GPIO.PWM(red, 100)     # use 100 Hz for all
pg = GPIO.PWM(green, 100)    
pb = GPIO.PWM(blue, 100)    
pr.start(0)                 # all initially off
pg.start(0)
pb.start(0)

try:
    while True:
        # ramp hue from 0 to 1
        steps = 200                 # number of steps in hue range
        for h in range(0, steps):
            # convert to RGB values (0-1)
            hue = h/steps
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)  # colours are fully saturated, max value

            # adjust PWM outputs
            pr.ChangeDutyCycle(rgb[0]*100)      # red
            pg.ChangeDutyCycle(rgb[1]*100)      # green
            pb.ChangeDutyCycle(rgb[2]*100)      # blue

            # delay 50 ms per step
            time.sleep(0.05)

except KeyboardInterrupt:
    pr.stop()
    pg.stop()
    pb.stop()
    GPIO.cleanup()
