import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x14.analog_in import AnalogIn
import board
import busio
import time

#TODO: create dictionary of conversion, units pairs

class Geophone():

    def __init__():
        
        self.init_gadc()
        self._conversion = 1 #mV


    def init_gadc(self):
        
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)
        self.chan = AnalogIn(ads, ADS.P1)

    @property(int)
    def adcGain(self) -> int:
        return self._gain

    @adsGain.setter(int)
    def adsGain(self, value: int):
        VALID_GAINS = {1, 2, 4, 8, 16}
        if value not in VALID_GAINS:
            raise ValueError(f'Gain value must be one of the following: {VALID_GAINS}')
        else:
            self._gain = value

    @property(float)
    def chanVoltage(self) -> float:
        return self.chan.voltage * self._conversion

    @property(int)
    def chanRaw(self) -> int:
        return self.chan.value

    @property(str)
    def units(self) -> str:
        return self._units

    @units.setter(str)
    def units(self, value->str):
        VALID_UNITS = {'raw', 'mv', 'v'}
        if value.lower() not in VALID_UNITS:
            raise ValueError(f'Units value must be one of the following: {VALID_UNITS})')
        else:
            self._units = value

    @property(int)
    def unitConversion(self) -> int:
        return self._conversion

    @unitConversion.setter(int)
    def unitConversion(self, value->int):
        self._conversion = value
