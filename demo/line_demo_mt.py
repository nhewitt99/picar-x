from picar.sensor import LineSensor
from picar.controller import LineController
from picar.utils import reset_mcu

reset_mcu()

from picar.multitask import Bus, Consumer, Producer
import concurrent.futures
import signal

from random import uniform
from time import sleep

TERM_BUS = Bus()


def handler(signum, frame):
    """
    Can't figure out why this doesn't work :(
    It doesn't get called with the first ctrl+c, only the second,
    and the written value doesn't propogate into the threads...
    """
    global TERM_BUS
    print("SIGINT caught!!")
    TERM_BUS.write("SIGINT")


def main():
    global TERM_BUS

    ls = LineSensor(mean=1000)
    lc = LineController()

    sensor_bus = Bus()
    sensor_bus.write((0.5,))

    # Non-dummy implementation
    #    produce_line = Producer(ls.detect_line, sensor_bus, term_bus, name="Sensor")
    #    consume_line = Consumer(lc.forward, sensor_bus, term_bus, name="Controller")

    def dummy_sense():
        x = uniform(-1, 1)
        print(f"Sensor output: {x:.3f}")
        return x

    def dummy_control(x):
        print(f"Control output: {x * 90.0:.2f}")

    # Dummy implementation for simple demo
    produce_line = Producer(dummy_sense, sensor_bus, TERM_BUS, name="Sensor")
    consume_line = Consumer(dummy_control, sensor_bus, TERM_BUS, name="Controller")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        signal.signal(signal.SIGINT, handler)
        eSensor = executor.submit(produce_line.main)
        eControl = executor.submit(consume_line.main)
    print(eSensor.result())
    print(eControl.result())


if __name__ == "__main__":
    main()
