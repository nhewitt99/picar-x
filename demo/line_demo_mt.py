from picar import Picarx
from picar.sensor import LineSensor
from picar.controller import LineController
from picar.utils import reset_mcu

reset_mcu()

from picar.multitask import Bus, Consumer, Producer
import concurrent.futures
import signal

from random import uniform

TERM_BUS = Bus()


def handler(signum, frame):
    global TERM_BUS
    TERM_BUS.write("SIGINT")


def main():
    global TERM_BUS
    signal.signal(signal.SIGINT, handler)

    px = Picarx()
    ls = LineSensor(mean=1000)
    lc = LineController()

    sensor_bus = Bus()

    #    produce_line = Producer(ls.detect_line, sensor_bus, term_bus, name="Sensor")
    #    consume_line = Consumer(lc.forward, sensor_bus, term_bus, name="Controller")

    def dummy_sense():
        return uniform(-1, 1)

    def dummy_control(arg):
        print(arg * 90.0)

    produce_line = Producer(dummy_sense, sensor_bus, TERM_BUS, name="Sensor")
    consume_line = Consumer(dummy_control, sensor_bus, TERM_BUS, name="Controller")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        eSensor = executor.submit(produce_line.main)
        eControl = executor.submit(consume_line.main)
    eSensor.result()
    eControl.result()


if __name__ == "__main__":
    main()
