from step_detection.base import BaseEstimator, BaseCost
from typing import List, Tuple, Any
import numpy as np


class EscalatorRush(BaseEstimator):
    def __init__(self,
                 cost: BaseCost,
                 min_step_size: int = 3,
                 max_dist: int = 2,
                 jump: int = 1) -> None:

        self.signal = []
        self.inds = []
        self.score = []
        self.min_step_size: int = min_step_size
        self.max_dist = max_dist
        self.jump = jump

        if cost is not None and isinstance(cost, BaseCost):
            self.cost = cost

    def fit(self, signal: List[float]) -> 'EscalatorRush':
        self.cost.fit(signal)
        self.signal = signal
        # indexes
        self.inds = np.arange(start=0, stop=len(signal)-self.min_step_size+1, step=self.jump)

        score = []
        for k in self.inds:
            error = self.cost.error(k, k+self.min_step_size)
            score.append(error)
        self.score = np.array(score)
        return self

    def predict(self) -> List[Tuple[int, int, Any]]:
        """
        :return: list of "stair" steps found [(start, stop, value)...]
        """
        good_inds = [self.inds[i] for i in range(len(self.inds)) if self.score[i] <= self.max_dist]

        potential_steps = []
        for index in good_inds:
            start: int = index
            end: int = index + self.min_step_size

            if not potential_steps or (potential_steps and start > potential_steps[-1][1]):
                while self.cost.error(start, end+1) <= self.max_dist and end < len(self.signal):
                    end += 1

                potential_steps.append((start, end, np.mean(self.signal[start:end-1])))

        return potential_steps
