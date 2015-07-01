#!/usr/bin/env python
#
# Wombat board support modules
#
#   v1.1    11/5/15
#           (reduced SPI xfer rate to 100kHz to work with Banana Pro)
#
#   David Meiklejohn
#   Gooligum Electronics
#
# Functions defined:
#   readadc(chan)       : returns value (0-1023) of ADC channel 'chan'
#   readbutton(n)       : returns 1 if pushbutton 'Sn' is pressed, 0 if not pressed
#   setled(n, state)    : sets led 'Dn' to 'state' - 1 = on, 0 = off
#   cleanup()           : resets GPIO pins to defaults
#

import RPi.GPIO as GPIO
import spidev


# Read an analog input
#
#   usage    : value = readadc(chan)
#
#   returns  : current value of ADC input channel 'chan'
#              (integer, 0-1023)
#
#   params   : chan = channel number, integer in range 0 - 7
#
#   requires : spidev module
#              MCP3008 on SPI bus 0, device 0
#
def readadc(chan):
    # open SPI device corresponding to MPC3008
    spi = spidev.SpiDev()
    spi.open(0, 0)          # MCP3008 is on bus 0, device 0

    if ((chan > 7) or (chan < 0)):
        raise ValueError("Channel number out of range")

    # transfer start bit (1), single/diff mode bit (1), channel number, 12 bits padding at 100kHz
    # returns 10-bit result with MSB in byte 1<1:0>, LSB in byte 2<7:0>
    adc_spi = spi.xfer([1,128+chan*16,0],100000)
    adc_out = (adc_spi[1]&3)*256+adc_spi[2]
    
    # cleanup SPI connection
    spi.close()

    return adc_out


# Read a button
#
#   usage    : value = readbutton(n)
#
#   returns  : value of pushbutton 'Sn'
#               = 1 (True)  if button pressed
#               = 0 (False) if button not pressed
#
#   params   : n = pushbutton number, integer in range 1 - 2
#
#   requires :  RPi.GPIO module
#               active-low pushbutton switches on GPIO24 and GPIO25
#
def readbutton(n):
    # pin assignments
    buttons = [24, 25]          # S1, S2 pins
    
    # configure GPIO module
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    if ((n > 2) or (n < 1)):
        raise ValueError("Button number out of range")

    # adjust index
    n -= 1                      # index into button list starts at 0, not 1

    # configure button pin
    GPIO.setup(buttons[n], GPIO.IN, pull_up_down=GPIO.PUD_UP)   # enable pull-up

    # button is active-low, so return with inverse of GPIO input
    return not(GPIO.input(buttons[n]))


# Turn an LED on or off
#
#   usage    : setled(n, state)
#
#   returns  : none
#
#   params   : n = LED number, integer in range 1 - 4
#              state = output state : 0 (False) = LED off
#                                     1 (True)  = LED on  
#
#   requires :  RPi.GPIO module
#               active-high LEDs on GPIO4, GPIO17, GPIO22 and GPIO23
#
def setled(n, state):
    # pin assignments
    leds = [4, 17, 22, 23]      # D1, D2, D3, D4 pins

    # configure GPIO module
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    if ((state != True) and (state != False)):
        raise ValueError("LED state must be 0 (False) or 1 (True)")

    if ((n > 4) or (n < 1)):
        raise ValueError("LED number out of range")

    # adjust index
    n -= 1                      # index into button list starts at 0, not 1

    # configure LED pin
    GPIO.setup(leds[n], GPIO.OUT)

    # set LED state
    GPIO.output(leds[n], state)

    return



# Cleanup I/O
#
#   Resets GPIO pins to defaults
#
#   usage    : cleanup()
#
#   returns  : none
#
#   params   : none
#
#   requires : RPi.GPIO module
#
def cleanup():
    GPIO.cleanup()

    return

