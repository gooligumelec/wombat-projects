#!/usr/bin/python3
#
# Demonstrates use of an ADC input to control LED brightness
#
# uses PWM output to control D1 on Wombat board (GPIO 4)
# with duty cycle set by analog input CH0 (pot RP1)
#
# outputs complementary PWM output on D2 (GPIO 17)
# (D1 lit while D2 off and vice versa)
#
#   v1.0    28/4/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import RPi.GPIO as GPIO
from wombat import readadc

# pin assignments
adc_chan = 0                # use analog input CH0
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
        # calculate duty cycle from current value (0-1023) of ADC input
        dc = readadc(adc_chan)/1023*100

        # adjust PWM outputs
        p1.ChangeDutyCycle(dc)
        p2.ChangeDutyCycle(100-dc)

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()
