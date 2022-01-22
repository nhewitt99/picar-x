from picamera import PiCamera
from time import sleep

with PiCamera() as camera:
    camera.resolution = (1024, 768)  # (640, 480)
    camera.framerate = 24
    camera.start_preview()
    sleep(2)       # warmup
    camera.capture('foo.png')
