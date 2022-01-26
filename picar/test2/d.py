from .b import B
from .c import C



class D(B,C):
    def __init__(self):
        super().__init__()


class E(C,B):
    def __init__(self):
        super().__init__()
