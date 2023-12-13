import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x14.analog_in import AnalogIn
import board
import busio
import time

#TODO: create dictionary of conversion, units pairs
#TODO: timestamp data

class Geophone():

    def __init__():
        
        self.init_gadc()
        self._conversion = 1 #mV


    def init_gadc(self):
        
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)
        self.chan = AnalogIn(ads, ADS.P1)
    
    @property(tuple[int, ...])
    def _validGains(self) -> tuple[int, ...]:
        return {2/3, 1, 2, 4, 8, 16}

    @property(int)
    def adcGain(self) -> int:
        return self._gain

    @adsGain.setter(int)
    def adsGain(self, value: int):
        if value not in self.validGains:
            raise ValueError(f'Gain value must be one of the following: {VALID_GAINS}')
        else:
            self._gain = value

    @property(float)
    def chanVoltage(self) -> float:
        return self.chan.voltage * self._conversion

    @property(int)
    def chanRaw(self) -> int:
        return self.chan.value

    @property(tuple[str, ...])
    def validUnits(self) -> tuple[str, ...]:
        return {'raw', 'mv', 'v'}

    @property(str)
    def units(self) -> str:
        return self._units

    @units.setter(str)
    def units(self, value->str):
        if value.lower() not in self.validUnits:
            raise ValueError(f'Units value must be one of the following: {VALID_UNITS})')
        else:
            self._units = value

    @property(int)
    def unitConversion(self) -> int:
        return self._conversion

    @unitConversion.setter(int)
    def unitConversion(self, value->int):
        self._conversion = value

    @property(int)
    def sampleTime(self) -> int:
        # sample time in ms
        return self._sampleTime

    @sampleTime.setter(float)
    def sampleTime(self, value:float):
        self._sampleTime = value

    def grabValue(self, sensorValue):
        self.buffer = []
        self.buffer.append(sensorValue)

    @property(list[float, ...])
    def buffer(self):
        return self.buffer
