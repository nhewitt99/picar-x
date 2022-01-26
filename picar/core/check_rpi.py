from os import uname


def check_rpi():
    low = [i.lower() for i in uname()]
    rpi = any(["rpi" in l for l in low])
    rasp = any(["rasp" in l for l in low])
    return rpi or rasp
