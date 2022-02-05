class UltrasonicController:
    """
    This class simply outputs true/false if a safe distance is ahead
    """

    def __init__(self, min_distance=20):
        """
        @param min_distance: threshold for ultrasonic distance, cm
        @type min_distance: float, int
        """
        self.min_distance = min_distance

    def forward(self, value):
        return value > self.min_distance
