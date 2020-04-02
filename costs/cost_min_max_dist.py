from step_detection.base import BaseCost


class DistanceMinMaxCost(BaseCost):
    def __init__(self):
        self.signal = None

    def fit(self, signal: list) -> 'DistanceMinMaxCost':
        """Set the internal parameter"""
        self.signal = signal
        return self

    def error(self, start: int, end: int) -> float:
        """Return the cost of a segment based on the distance between the min and max"""
        sub = self.signal[start:end]
        return max(sub) - min(sub)
