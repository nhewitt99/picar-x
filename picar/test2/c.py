from .b import B

class C(B):
    def __init__(self):
        super().__init__()
        print('init C')
