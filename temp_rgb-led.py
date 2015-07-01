#!/usr/bin/python3
#
# Use temperature sensor to control the colour of an RGB LED
#
# uses PWM outputs to adjust brightness of RGB components
# with hue set by MCP9700 sensor on analog input CH2
#
#   v1.0    6/5/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import RPi.GPIO as GPIO
from wombat import readadc
import colorsys

# pin assignments
adc_chan = 2                # MCP9700 temp sensor on analog input CH2
red = 23                    # red LED on GPIO 23 (active high)
green = 22                  # green LED on GPIO 22 (active high)
blue = 27                   # blue LED on GPIO 27 (active high)

# constants
min_temp = 20               # min and max temps (deg C) for display range
max_temp = 40

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
        # convert ADC input level (0 - 1023) to temperature (-50 - 280 deg C)
        temp = (readadc(adc_chan)*3.3/1023 - 0.5) * 100

        # map temperature to hue
        #   min_temp corresponds to hue = 0,
        #   max_temp corresponds to hue = 1
        if temp < min_temp:
            hue = 0
        elif temp > max_temp:
            hue = 1
        else:
            hue = (temp - min_temp) / (max_temp - min_temp)

        # convert hue to RGB values (0-1)
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)  # colours are fully saturated, max value

        # adjust PWM outputs
        pr.ChangeDutyCycle(rgb[0]*100)      # red
        pg.ChangeDutyCycle(rgb[1]*100)      # green
        pb.ChangeDutyCycle(rgb[2]*100)      # blue

except KeyboardInterrupt:
    pr.stop()
    pg.stop()
    pb.stop()
    GPIO.cleanup()
