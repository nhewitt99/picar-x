#!/usr/bin/env python3
from picar.dummy import ADC as ADC_base

class ADC(ADC_base):
    def __init__(self, chn):
        super().__init__(chn)

    def read(self):
        # self._debug("Write 0x%02X to 0x%02X"%(self.chn, self.ADDR))
        # self.bus.write_byte(self.ADDR, self.chn)
        self.send([self.chn, 0, 0], self.ADDR)

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_h = self.bus.read_byte(self.ADDR)
        value_h = self.recv(1, self.ADDR)[0]

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_l = self.bus.read_byte(self.ADDR)
        value_l = self.recv(1, self.ADDR)[0]

        value = (value_h << 8) + value_l
        # self._debug("Read value: %s"%value)
        return value
