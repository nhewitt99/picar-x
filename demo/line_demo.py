from picar import Picarx
from picar.sensor.line_sensor import LineSensor
from picar.controller.line_controller import LineController
from picar.utils import reset_mcu
reset_mcu()

from time import sleep


def main():
    px = Picarx()
    ls = LineSensor(mean=1000)
    lc = LineController()

    speed = 0

    try:
        while True:
            sense = ls.detect_line()
            angle = lc.forward(sense)
            px.move(speed, angle)

            print(angle)
            sleep(0.1)
    except KeyboardInterrupt:
        print('ending!')


if __name__=='__main__':
    main()
