from picar.test1 import A

class B(A):
    def __init__(self):
        super().__init__()
        print('init B')
