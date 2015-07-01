#!/usr/bin/python3
#
# Demonstrates PWM control of LED brightness
#
# ramps PWM output on D1 on Wombat board (GPIO 4)
# with complementary PWM output on D2 (GPIO 17)
# (D1 lit while D2 off and vice versa)
#
#   v1.0    28/4/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import RPi.GPIO as GPIO
import time

# pin assignments
led1 = 4                    # LED D1 on GPIO 4 (active high)
led2 = 17                   # LED D2 on GPIO 17 (active high)

# configure I/O
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# configure pins
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

# setup PWM outputs
p1 = GPIO.PWM(led1, 100)    # use 100 Hz for both
p2 = GPIO.PWM(led2, 100)    
p1.start(0)                 # D1 initially off
p2.start(100)               # D2 initially on (duty cycle = 100)

try:
    while True:
        # ramp up duty cycle from 0 to 100
        for dc in range(0, 101, 5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(100-dc)
            time.sleep(0.05)                # 50ms per step
        # ramp duty cycle back down to 0
        for dc in range(100, -1, -5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(100-dc)
            time.sleep(0.05)                # 50ms per step

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()
