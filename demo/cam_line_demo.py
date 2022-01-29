from picar import Picarx
from picar.sensor import LaneCamera
from picar.controller import LineController
from picar.utils import reset_mcu

reset_mcu()

from time import sleep


def main():
    px = Picarx()
    cam = LaneCamera()
    lc = LineController()

    speed = 0

    try:
        while True:
            sense = ls.detect_lane()
            angle = lc.forward(sense)
            px.move(speed, angle)

            print(angle)
            sleep(0.1)
    except KeyboardInterrupt:
        print("ending!")


if __name__ == "__main__":
    main()
