class Pin(object):
    # Magic numbers input manually since GPIO can't be imported without pi
    OUT = 0
    IN = 1
    IRQ_FALLING = 32
    IRQ_RISING = 31
    IRQ_RISING_FALLING = 33
    PULL_UP = 22
    PULL_DOWN = 21
    PULL_NONE = None

    _dict_1 = {
        "D0": 17,
        "D1": 18,
        "D2": 27,
        "D3": 22,
        "D4": 23,
        "D5": 24,
        "D6": 25,
        "D7": 4,
        "D8": 5,
        "D9": 6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW": 19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    def __init__(self, *value):
        super().__init__()

        self._dict = self._dict_1

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
                self._pin = self._dict[pin]
            except Exception as e:
                print(e)
                self._error("Pin should be in %s, not %s" % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            self._pin = pin
        else:
            self._error("Pin should be in %s, not %s" % (self._dict.keys(), pin))

        self._value = 0
        self.init(mode, pull=setup)

        print(f"Dummy pin: set up {value}")

    def _error(self, str):
        raise Exception(str)

    def check_board_type(self):
        pass

    def init(self, mode, pull=PULL_NONE):
        self._pull = pull
        self._mode = mode

    def dict(self, *_dict):
        pass

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            self.mode(self.IN)
            return 1  # Dummy high value
        else:
            value = value[0]
            self.mode(self.OUT)
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return self._mode
        else:
            mode = value[0]
            self._mode = mode

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)
        print("Dummy pin: set interrupt (but not really!)")

    def name(self):
        return "GPIO%s" % self._pin

    def names(self):
        return [self.name, self._board_name]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4 = 4
        GPIO5 = 5
        GPIO6 = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass


if __name__ == "__main__":
    import time

    mcu_reset = Pin("MCURST")
    mcu_reset.off()
    time.sleep(0.001)
    mcu_reset.on()
    time.sleep(0.01)
