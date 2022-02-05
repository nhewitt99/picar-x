import time
from picar.core import Pin


class UltrasonicSensor:
    def __init__(self, trig, echo, timeout=0.02):
        self.trig, self.echo = Pin(trig), Pin(echo)
        self.timeout = timeout

    # Copied directly from picar legacy code
    def _read(self):
        # Send a pulse
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()

        # Use sensor's ECHO pin to determine ToF
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value() == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value() == 1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1

        # Mathemagically convert ToF to centimeters
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, attempts=10):
        for i in range(attempts):
            dist = self._read()
            if dist != -1 and a <= 300:  # they had 'or' here which is wrong
                return dist
        return -1
