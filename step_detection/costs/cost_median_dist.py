import numpy as np
from step_detection.base import BaseCost


class DistanceMedianCost(BaseCost):
    def __init__(self):
        self.signal = None

    def fit(self, signal: list) -> 'DistanceMedianCost':
        """Set the internal parameter"""
        self.signal = signal
        return self

    def error(self, start: int, end: int) -> float:
        """Return the cost of a segment based on the distance furthest element from the median"""
        sub = self.signal[start:end]
        median = np.median(sub)
        dist_max = max(sub) - median
        dist_min = median - min(sub)
        return max(dist_max, dist_min)