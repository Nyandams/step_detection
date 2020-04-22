import abc
from typing import List, Tuple, Any
import numpy as np


class BaseCost(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fit') and
                callable(subclass.fit) and
                hasattr(subclass, 'error') and
                callable(subclass.error))

    @abc.abstractmethod
    def fit(self, *args, **kwargs):
        """Set the parameters of the cost function"""
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, start: int, end: int):
        """
        Return the cost on segment [start:end]
        :param start: start of the segment
        :param end: end of the segment
        """
        raise NotImplementedError


class BaseEstimator(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fit') and
                callable(subclass.fit) and
                hasattr(subclass, 'predict') and
                callable(subclass.predict))

    @abc.abstractmethod
    def fit(self, *args, **kwargs):
        """Set the signal to segment"""
        raise NotImplementedError

    @abc.abstractmethod
    def predict(self, *args, **kwargs):
        """To call the segmentation algorithm"""
        raise NotImplementedError


def group_steps(steps: List[Tuple[int, int, Any]], signal: List[float], gap: int = 3, dist: int = 2):
    """
    Regroup 2 steps together
    :param steps: steps that results from any algorithm
    :param signal: original time signal
    :param gap: distance in 'time' between 2 steps (maximum index difference between 2 steps)
    :param dist: distance allowed between 2 values of steps
    :return: a new list of steps  List[Tuple[int, int, Any]]
    """
    i: int = 0
    grouped_step: List[Tuple[int, int, Any]] = []
    precedent = None
    while i < len(steps):
        if not precedent and i == (len(steps) - 1):
            grouped_step.append(steps[i])
        elif not precedent:
            precedent = steps[i]
        elif steps[i][0] - precedent[1] < gap and abs(steps[i][2] - precedent[2]) < dist and i == len(steps) - 1:
            grouped_step.append((precedent[0], steps[i][1], np.mean(signal[precedent[0]:steps[i][1]])))
        elif steps[i][0] - precedent[1] < gap and abs(steps[i][2] - precedent[2]) < dist:
            precedent = (precedent[0], steps[i][1], np.mean(signal[precedent[0]:steps[i][1]]))
        elif i == len(steps) - 1:
            grouped_step.append(precedent)
            grouped_step.append(steps[i])
        else:
            grouped_step.append(precedent)
            precedent = steps[i]

        i += 1

    return grouped_step
