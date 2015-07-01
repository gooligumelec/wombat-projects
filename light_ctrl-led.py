#!/usr/bin/python3
#
# Use light level (measured by a photocell) to control the brightness of an LED
# while automatically turning another LED on and off
#
# uses PWM output to control LED D1 on Wombat board (GPIO 4)
# with duty cycle set by analog input CH1
# (connected to photocell/resistor divider)
#
# lights LED D2 (GPIO 17) only if analog input CH1 < threshold
# (D2 lit only when photocell is in darkness)
#
#   v1.1    6/5/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import RPi.GPIO as GPIO
from wombat import readadc

# pin assignments
adc_chan = 1                # LDR is on analog input CH1
led1 = 4                    # LED D1 on GPIO 4 (active high)
led2 = 17                   # LED D2 on GPIO 17 (active high)

# constants
threshold = 50              # light level to turn on/off LED

# configure I/O
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# configure pins
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

# setup PWM outputs
p1 = GPIO.PWM(led1, 100)    # use 100 Hz
p1.start(0)                 # D1 initially off

try:
    while True:
        # derive light level (0-100) from current value (0-1023) of ADC input
        light_level = readadc(adc_chan)/1023*100

        # adjust PWM output on LED 1
        # (duty cycle is inverse of light level -> bright LED in low light)
        p1.ChangeDutyCycle(100-light_level)

        # turn on LED 2 if light level below threshold
        GPIO.output(led2, light_level < threshold)

except KeyboardInterrupt:
    p1.stop()
    GPIO.cleanup()
