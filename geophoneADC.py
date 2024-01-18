#! /usr/bin/env python

##########################################################
# geophoneADC.py
#
# A RaspberryPi application for reading the ADC values of
# a geophone.
#
#   Created: 12/09/23
#       - Kyle Leleux
#
#   Modified:
#
#   TODO:
#       - Add real-time plotting if possible 
#       - Added button toggle that stops and starts reading
#       - Add PyQt Display
#
#   NOTE:
#       1) Raspberry Pi does NOT have ADC, need to use a breakout board
#           - ADS1115
#       2) The ADS1015 and ADS1115 both have the same gain options.
#          
#                GAIN    RANGE (V)
#                ----    ---------
#                 2/3    +/- 6.144
#                   1    +/- 4.096
#                   2    +/- 2.048
#                   4    +/- 1.024
#                   8    +/- 0.512
#                  16    +/- 0.256
#          
##########################################################

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio
import pigpio
import time

##########################################################
# ADC Setup
##########################################################
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
# Think we can anticipate very low signals
ads.gain = 16
chan = AnalogIn(ads, ADS.P0)

while (True):
    print(f'voltage reading : {chan.voltage}mV')
