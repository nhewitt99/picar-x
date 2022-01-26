from .pin_dummy import Pin as Pin_dummy
import RPi.GPIO as GPIO


class Pin(Pin_dummy):
    OUT = GPIO.OUT
    IN = GPIO.IN
    IRQ_FALLING = GPIO.FALLING
    IRQ_RISING = GPIO.RISING
    IRQ_RISING_FALLING = GPIO.BOTH
    PULL_UP = GPIO.PUD_UP
    PULL_DOWN = GPIO.PUD_DOWN
    PULL_NONE = None

    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_2 = {
        "D0": 17,
        "D1": 4,  # Changed
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,  # Removed
        "D7": 4,  # Removed
        "D8": 5,  # Removed
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 25,  # Changed
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 5,  # Changed
    }

    def __init__(self, *value):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.check_board_type()

        if len(value) > 0:
            pin = value[0]
        else:
            pin = value

        if len(value) > 1:
            mode = value[1]
        else:
            mode = None

        if len(value) > 2:
            setup = value[2]
        else:
            setup = None

        if isinstance(pin, str):
            try:
                self._board_name = pin
                self._pin = self.dict()[pin]
            except Exception as e:
                print(e)
                self._error("Pin should be in %s, not %s" % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            self._pin = pin
        else:
            self._error("Pin should be in %s, not %s" % (self._dict.keys(), pin))

        self._value = 0
        self.init(mode, pull=setup)
        # self._info("Pin init finished.")

    def check_board_type(self):
        type_pin = self.dict()["BOARD_TYPE"]
        GPIO.setup(type_pin, GPIO.IN)
        if GPIO.input(type_pin) == 0:
            self._dict = self._dict_1
        else:
            self._dict = self._dict_2

    def init(self, mode, pull=PULL_NONE):
        self._pull = pull
        self._mode = mode
        if mode != None:
            if pull != None:
                GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                GPIO.setup(self._pin, mode)

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s'
                    % _dict
                )

    def value(self, *value):
        if len(value) == 0:
            self.mode(self.IN)
            result = GPIO.input(self._pin)
            # self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:
            value = value[0]
            self.mode(self.OUT)
            GPIO.output(self._pin, value)
            return value

    def mode(self, *value):
        if len(value) == 0:
            return self._mode
        else:
            mode = value[0]
            self._mode = mode
            GPIO.setup(self._pin, mode)

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)
        GPIO.add_event_detect(
            self._pin, trigger, callback=handler, bouncetime=bouncetime
        )


if __name__ == "__main__":
    import time

    mcu_reset = Pin("MCURST")
    mcu_reset.off()
    time.sleep(0.001)
    mcu_reset.on()
    time.sleep(0.01)
