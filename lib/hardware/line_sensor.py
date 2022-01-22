from sensor import Sensor
from utils import reset_mcu
reset_mcu()

import numpy as np
from tqdm import tqdm

'''
    Notes:
    A0, A1, A2 -> left, center, right
    Higher value = more reflectivity
    TAPE:
        means: 1540.87 1550.26 1531.74
        stds:     2.87    2.86    2.98
    TILE:
        means: 1537.02 1547.79 1526.54
        stds:     2.44    2.97    3.08
'''

class LineSensor(Sensor):
    def __init__(self, sensitivity=1, black_on_white=True, pins=['A0', 'A1', 'A2']):
        super().__init__(pins)
        self.sensitivity = sensitivity
        self.black_on_white = black_on_white


if __name__=='__main__':
    ls = LineSensor()

    n = 10000
    vals = np.zeros((n, 3))

    for i in tqdm(range(n)):
        vals[i,:] = ls.poll_raw()

    np.set_printoptions(precision=2)
    print(f'Means: {np.mean(vals, axis=0)}')
    print(f'Stds:  {np.std(vals, axis=0)}')
