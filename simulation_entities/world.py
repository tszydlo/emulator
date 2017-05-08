from abc import ABC, abstractmethod


class WorldEntity(ABC):

    @abstractmethod
    def transformation(self):
        pass

    @abstractmethod
    def start_transformation(self):
        pass