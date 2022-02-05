from picar.sensor import LineSensor
from picar.controller import LineController
from picar.utils import reset_mcu

reset_mcu()

from picar.rossros.rossros import Bus, Consumer, Producer, Timer, runConcurrently
import concurrent.futures

from random import uniform
from time import sleep


def main():
    ls = LineSensor(mean=1000)
    lc = LineController()

    term_bus = Bus(False, "Timer Bus")
    sensor_bus = Bus(0.5, "Sensor Bus")

    # Non-dummy implementation
    #    produce_line = Producer(ls.detect_line, sensor_bus, term_bus, name="Sensor")
    #    consume_line = Consumer(lc.forward, sensor_bus, term_bus, name="Controller")

    def dummy_sense():
        x = uniform(-1,1)
        print(f"Sensor output: {x:.3f}")
        return x

    def dummy_control(x):
        print(f"Control output: {x * 90.0:.2f}")

    # Dummy implementation for simple demo
    produce_line = Producer(dummy_sense, sensor_bus, 0, term_bus, name="Sensor")
    consume_line = Consumer(dummy_control, sensor_bus, 0, term_bus, name="Controller")
    timer = Timer(term_bus, 5, 0.01, term_bus)

    runConcurrently([produce_line, consume_line, timer])


if __name__ == "__main__":
    main()
