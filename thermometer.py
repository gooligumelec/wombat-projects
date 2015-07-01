#!/usr/bin/python3
#
# Simple thermometer
#
# Continually prints temperature sensed by MCP9700
#  on Wombat board analog input 2
#  in degrees Celsius and Fahrenheit
#
#   v1.0    6/5/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import time
from wombat import readadc

adc_chan = 2        # MPC9700 temp sensor is on analog input CH2

try:
  while True:
    # get current voltage (0-3.3V) on ADC input
    Vout = readadc(adc_chan)*3.3/1024

    # convert voltage to temperature in degrees C and F
    TempC = (Vout - 0.5) * 100
    TempF = TempC * 9/5 + 32

    print("temperature = %4.1f C" % TempC, "= %4.1f F" % TempF)
    time.sleep(0.5)

except KeyboardInterrupt:
  print("done")

