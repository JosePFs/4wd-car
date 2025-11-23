from abc import ABC, abstractmethod


class ObstaclesDetectorDistance(ABC):

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def get_distance(self) -> float:
        ...
