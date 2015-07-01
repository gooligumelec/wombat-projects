#!/usr/bin/python3
#
# Simple light meter
#
# Continually prints light level detected by LDR/resistor divider
#  on Wombat board analog input 1
#  as percentage between 0 (dark) and 100 (bright light)
#
#   v1.0    3/5/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import time
from wombat import readadc

adc_chan = 1        # LDR is on analog input CH1

try:
  while True:
    # get current value (0-1023) of ADC input
    adc_out = readadc(adc_chan)

    light_level = (adc_out * 100)/1023
    print("light level = %4.1f %%" % (light_level))
    time.sleep(0.5)

except KeyboardInterrupt:
  print("done")

