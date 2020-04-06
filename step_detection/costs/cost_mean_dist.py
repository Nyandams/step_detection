import numpy as np
from step_detection.base import BaseCost


class DistanceMeanCost(BaseCost):
    def __init__(self):
        self.signal = None

    def fit(self, signal: list) -> 'DistanceMeanCost':
        """Set the internal parameter"""
        self.signal = signal
        return self

    def error(self, start: int, end: int) -> float:
        """Return the cost of a segment based on the distance furthest element from the median"""
        sub = self.signal[start:end]
        mean = np.mean(sub)
        dist_max = max(sub) - mean
        dist_min = mean - min(sub)
        return max(dist_max, dist_min)