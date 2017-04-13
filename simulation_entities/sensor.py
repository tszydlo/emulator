import itertools
from abc import ABC, abstractmethod


class Sensor(ABC):
    @property
    @abstractmethod
    def default_formula(self):
        pass

    @property
    @abstractmethod
    def function_generator(self):
        pass

    @abstractmethod
    def apply_formula(self, formula):
        pass

    @function_generator.setter
    def function_generator(self, generator):
        self._function_generator = generator

    def get_measurement(self):
        return self.function_generator.__next__()


class HumiditySensor(Sensor):
    @property
    def function_generator(self):
        return self._function_generator

    @property
    def default_formula(self):
        return lambda x: x * 10

    def apply_formula(self, formula):
        self._function_generator = (formula(x) for x in itertools.count())

    def __init__(self):
        self._function_generator = (self.default_formula(x) for x in itertools.count())
