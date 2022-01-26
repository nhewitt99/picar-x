class LineController:
    def __init__(self, angle_lims=[-30, 30]):
        self.range = angle_lims[1] - angle_lims[0]
        self.mid = (angle_lims[1] + angle_lims[0]) / 2

    # Proportional mapping for now
    def forward(self, value):
        value = -1.0 if value < -1.0 else value
        value = 1.0 if value > 1.0 else value
        return self.mid + (value * self.range)
