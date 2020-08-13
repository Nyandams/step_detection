from step_detection.base import BaseEstimator, BaseCost
from typing import List, Tuple, Any
import numpy as np


class EscalatorRush(BaseEstimator):
    def __init__(self,
                 cost: BaseCost,
                 min_step_size: int = 3,
                 max_dist: float = 2,
                 jump: int = 1,
                 cache_size: int = None) -> None:
        """
        This estimator can use any cost class from the library, but the use of 'DistanceMeanCost' is encouraged.
        Several optimization parameters can be used (jump and cache_size)
        :param cost: the cost function
        :param min_step_size: the minimal size of a step
        :param max_dist: distance at which we consider a point isn't in the current step
        :param jump: ignore some indexes during the fitting of the data, the highest, the more indexes you'll jump over.
        Improve the speed of execution but reduce the execution time.
        :param cache_size: number of elements in the step at which moment we decide to use a cached value of the mean of
        the step instead of the cost function. Improve a lot the performances.
        """
        self.signal = []
        self.inds = []
        self.score = []
        self.min_step_size: int = min_step_size
        self.max_dist = max_dist
        self.jump = jump
        self.cache_size = cache_size
        self.cached_reference = {}

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
        good_inds = [idx for i, idx in enumerate(self.inds) if self.score[i] <= self.max_dist]
        potential_steps = []
        for index in good_inds:
            end: int = index + self.min_step_size

            if not potential_steps or (potential_steps and index >= potential_steps[-1][1]):
                while end < len(self.signal) and self.cached_cost_test(index, end):
                    end += 1

                potential_steps.append((index, end, np.mean(self.signal[index:end-1])))

        return potential_steps

    def cached_cost_test(self, start, end):
        if self.cache_size and start in self.cached_reference:
            return abs(self.signal[end] - self.cached_reference[start]) <= self.max_dist
        else:
            error = self.cost.error(start, end+1)
            if self.cache_size and end - start >= self.cache_size and error <= self.max_dist:
                self.cached_reference[start] = np.mean(self.signal[start])
            return error <= self.max_dist
