from .sensor import Sensor

import numpy as np
from tqdm import tqdm
from math import exp

"""
    Notes:
    A0, A1, A2 -> left, center, right
    Higher value = more reflectivity
    TAPE:
        means: 1540.87 1550.26 1531.74
        stds:     2.87    2.86    2.98
    TILE:
        means: 1537.02 1547.79 1526.54
        stds:     2.44    2.97    3.08
    CARPET:
        1400ish
    ELECTRICAL_TAPE:
        700ish
"""


def sigmoid(alpha):
    return 1.0 / (1 + exp(alpha))


class LineSensor(Sensor):
    # TODO: proper docstrings
    # Sensitivity is defined by a sigmoid function:
    # Lower values of scaling results in smoother curve -> less "decisive"
    # Mean is cutoff value between a line and no line
    # Black_on_white will cause lower reflection to be a line
    # Pins are left-to-right
    def __init__(
        self, scaling=0.05, mean=1400, black_on_white=True, pins=["A0", "A1", "A2"]
    ):
        super().__init__(pins)
        self.scaling = scaling
        self.mean = mean
        self.black_on_white = black_on_white

    # Use a sigmoid to smooth line strength
    def detect(self, value):
        alpha = self.scaling * (value - self.mean)
        confidence = sigmoid(alpha)

        # If black on white, high reflection = no line
        if self.black_on_white:
            confidence = 1 - confidence

        return confidence

    # Combine three confidences into a direction
    def direction(self, values):
        total = sum(values)
        if total == 0:
            return 0
        else:
            return -1 * (values[0] / total) + 1 * (values[2] / total)

    # Outward-facing function that returns a line position
    def detect_line(self):
        vals = self.poll_raw()
        confidences = [self.detect(v) for v in vals]
        return self.direction(confidences)


if __name__ == "__main__":
    ls = LineSensor()

    #    print(ls.detect(1300), ls.detect(1500))
    #    print(ls.direction([0.1, 0.5, 0.5]))
    #    print(ls.direction([1.0, 0.1, 0.1]))

    n = 1000
    vals = np.zeros((n, 3))

    for i in tqdm(range(n)):
        vals[i, :] = ls.poll_raw()

    np.set_printoptions(precision=2)
    print(f"Means: {np.mean(vals, axis=0)}")
    print(f"Stds:  {np.std(vals, axis=0)}")
