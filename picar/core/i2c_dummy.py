# from .basic import _Basic_class
from smbus import SMBus


class I2C(object):
    MASTER = 0
    SLAVE = 1
    RETRY = 5

    def __init__(self, *args, **kargs):
        super().__init__()
        self._bus = 1

    def _i2c_write_byte(self, addr, data):
        pass

    def _i2c_write_byte_data(self, addr, reg, data):
        pass

    def _i2c_write_word_data(self, addr, reg, data):
        pass

    def _i2c_write_i2c_block_data(self, addr, reg, data):
        pass

    def _i2c_read_byte(self, addr):
        return bytes(0)

    def _i2c_read_i2c_block_data(self, addr, reg, num):
        return []

    def is_ready(self, addr):
        addresses = self.scan()
        if addr in addresses:
            return True
        else:
            return False

    def scan(self):
        return []

    def send(self, send, addr, timeout=0):
        pass

    def recv(self, recv, addr=0x00, timeout=0):
        if isinstance(recv, int):
            result = bytearray(recv)
        elif isinstance(recv, bytearray):
            result = recv
        else:
            return False
        for i in range(len(result)):
            result[i] = self._i2c_read_byte(addr)
        return result

    def mem_write(
        self, data, addr, memaddr, timeout=5000, addr_size=8
    ):  # memaddr match to chn
        if isinstance(data, bytearray):
            data_all = list(data)
        elif isinstance(data, list):
            data_all = data
        elif isinstance(data, int):
            data_all = []
            data = "%x" % data
            if len(data) % 2 == 1:
                data = "0" + data
            # print(data)
            for i in range(0, len(data), 2):
                # print(data[i:i+2])
                data_all.append(int(data[i : i + 2], 16))
        else:
            raise ValueError(
                "memery write require arguement of bytearray, list, int less than 0xFF"
            )
        # print(data_all)
        self._i2c_write_i2c_block_data(addr, memaddr, data_all)

    def mem_read(self, data, addr, memaddr, timeout=5000, addr_size=8):
        if isinstance(data, int):
            num = data
        elif isinstance(data, bytearray):
            num = len(data)
        else:
            return False
        result = bytearray(self._i2c_read_i2c_block_data(addr, memaddr, num))
        return result

    def readfrom_mem_into(self, addr, memaddr, buf):
        buf = self.mem_read(len(buf), addr, memaddr)
        return buf

    def writeto_mem(self, addr, memaddr, data):
        self.mem_write(data, addr, memaddr)
