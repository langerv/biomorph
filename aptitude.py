import abc
from enum import Enum

class PhysicalAptitudes(Enum):
    PERC = 1
    MOVE = 2
    CONS = 3

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__

class PsychicalAptitudes(Enum):
    INTL = 6
    CHAR = 7
    ETHQ = 8

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__

class AptitudeBase(abc.ABC):
    def __init__(self, value):
        self._value = value

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        self.Value = value

    @abc.abstractmethod
    def update(self):
        pass
