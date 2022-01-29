from time import sleep
from readerwriterlock import rwlock


class Bus:
    def __init__(self):
        self.msg = None
        self.lock = rwlock.RWLockWriteD()

    def write(self, msg):
        # All inputs as tuples! This will allow unpacking into functions
        assert isinstance(msg, tuple)
        with self.lock.gen_wlock():
            self.msg = msg

    def read(self):
        with self.lock.gen_rlock():
            return self.msg


class MultitaskDummy:
    def __init__(self, fn, bus, term, delay=0.05, name="foo"):
        """
        @param fn: The function to repeatedly execute
        @param input: The bus from which to 'consume' or 'produce'
        @param term: A bus used exclusively for terminate signals
        @param delay: Delay per loop
        """
        assert isinstance(bus, Bus)
        assert isinstance(term, Bus)

        self.fn = fn
        self.bus = bus
        self.term = term
        self.delay = delay
        self.name = name


class Consumer(MultitaskDummy):
    def __init__(self, fn, bus, term, delay=0.05, name="foo"):
        super().__init__(fn, bus, term, delay, name)

    def main(self):
        # Guarantee running at least once
        term_val = None

        while term_val is None:
            input_val = self.bus.read()

            if input_val is not None:
                self.fn(*input_val)

            term_val = self.term.read()
            sleep(self.delay)

        print(f"Consumer {self.name} terminating after receiving {term_val}")


class Producer(MultitaskDummy):
    def __init__(self, fn, bus, term, delay=0.05, name="bar"):
        super().__init__(fn, bus, term, delay, name)

    def main(self):
        # Guarantee running at least once
        term_val = None

        while term_val is None:
            out_val = self.fn()

            if isinstance(out_val, tuple):
                self.bus.write(out_val)
            else:
                self.bus.write((out_val,))

            term_val = self.term.read()
            sleep(self.delay)

        print(f"Producer {self.name} terminating after receiving {term_val}")


class ConsumerProducer(MultitaskDummy):
    def __init__(self, fn, bus_in, bus_out, term, delay=0.05, name="foobar"):
        super().__init__(fn, bus_in, term, delay, name)
        self.bus_in = bus_in
        self.bus_out = bus_out
        # Note that self.bus also redundantly exists = bus_in :(

    def main(self):
        # Guarantee running at least once
        term_val = None

        while term_val is None:
            input_val = self.bus_in.read()

            if input_val is not None:
                out_val = self.fn(*input_val)

                if isinstance(out_val, tuple):
                    self.bus_out.write(out_val)
                else:
                    self.bus_out.write((out_val,))

            term_val = self.term.read()
            sleep(self.delay)

        print(f"ConProd {self.name} terminating after receiving {term_val}")
