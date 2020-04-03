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
        self.inds = np.arange(start=0, stop=len(signal)-self.min_step_size, step=self.jump)

        score = []
        for k in self.inds:
            error = self.cost.error(k, k+self.min_step_size-1)
            score.append(error)
        self.score = np.array(score)
        return self

    @staticmethod
    def __remove_redundant(steps: List[Tuple[int, int, Any]]) -> List[Tuple[int, int, float]]:
        """
        TODO: better algo
        :param steps:
        :return:
        """
        if not steps:
            return []
        end = steps[0][1]
        indexes_to_keep = [0]
        for i, step in enumerate(steps):
            if step[0] > end:
                indexes_to_keep.append(i)

                end = step[1]
        return [steps[i] for i in range(len(steps)) if i in indexes_to_keep]

    def predict(self) -> List[Tuple[int, int, Any]]:
        """
        :return: list of "stair" steps found [(start, end, value)...]
        """
        good_inds = [self.inds[i] for i in range(len(self.inds)) if self.score[i] <= self.max_dist]

        potential_steps = []
        for index in good_inds:
            start: int = index
            end: int = index + self.min_step_size - 1

            while self.cost.error(start, end) <= self.max_dist and end < good_inds[-1] + self.min_step_size - 1:
                """good_inds[-1] + self.min_step_size - 1 : to remove useless processing"""
                end += 1

            potential_steps.append((start, end-1, np.mean(self.signal[start:end-1])))

        return self.__remove_redundant(potential_steps)
