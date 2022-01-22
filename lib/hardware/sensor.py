from adc import ADC


class Sensor(object):
    def __init__(self, pins):
        self.channels = [ADC(pin) for pin in pins]

    def poll_raw(self):
        return [chn.read() for chn in self.channels]

