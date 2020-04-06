import abc
from typing import List, Tuple, Any

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
