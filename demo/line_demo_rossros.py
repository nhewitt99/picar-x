from picar.sensor import LineSensor, UltrasonicSensor
from picar.controller import LineController, UltrasonicController
from picar.utils import reset_mcu
from picar import Picarx

reset_mcu()

from picar.rossros.rossros import (
    Bus,
    ConsumerProducer,
    Consumer,
    Producer,
    Timer,
    runConcurrently,
)
import concurrent.futures

from random import uniform
from time import sleep


class LineUltraController:
    """
    Simple class to combine an angle and a "safe to drive" value
    to send motor controls to a picar
    """

    def __init__(self):
        self.picar = Picarx()

    def forward(self, angle, safe):
        if safe:
            print(f"Moving forward with angle {angle}")
            self.picar.move(0.3, angle)
        else:
            print("Stopped!")
            self.picar.stop()


def main():
    ls = LineSensor(mean=1000)
    lc = LineController()
    us = UltrasonicSensor("D2", "D3")
    uc = UltrasonicController()
    luc = LineUltraController()

    term_bus = Bus(False, "Timer Bus")

    # Raw sensor data
    line_bus = Bus(0.5, "Line Bus")
    ultra_bus = Bus(100, "Ultra Bus")

    # Data interpreted by controllers
    angle_bus = Bus(0.0, "Angle Bus")
    safe_bus = Bus(True, "Safety Bus")

    # True to run tests with actual values off hardware
    dummy = True

    def dummy_line():
        x = uniform(-1, 1)
        return x

    def dummy_ultra():
        x = uniform(0, 200)
        return x

    if dummy:
        produce_line = Producer(dummy_line, line_bus, 0, term_bus, name="Line Sensor")
        produce_ultra = Producer(
            dummy_ultra, ultra_bus, 0, term_bus, name="Ultra Sensor"
        )
    else:
        produce_line = Producer(ls.detect_line, line_bus, term_bus, name="Line Sensor")
        produce_ultra = Producer(us.read, ultra_bus, term_bus, name="Ultra Sensor")

    # Controllers take raw sensor data and return more informative info
    consume_line = ConsumerProducer(
        lc.forward, line_bus, angle_bus, 0, term_bus, name="Line Controller"
    )
    consume_ultra = ConsumerProducer(
        uc.forward, ultra_bus, safe_bus, 0, term_bus, name="Ultra Controller"
    )

    run_car = Consumer(
        luc.forward, (angle_bus, safe_bus), 0, term_bus, name="Car Controller"
    )
    timer = Timer(term_bus, 20, 0.01, term_bus)

    runConcurrently(
        [produce_line, consume_line, produce_ultra, consume_ultra, run_car, timer]
    )


if __name__ == "__main__":
    main()
