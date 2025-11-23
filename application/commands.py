from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain import Car
    from domain import ObstaclesDetector


class CarCommand(ABC):
    @abstractmethod
    def execute(self, car: 'Car') -> None:
        ...


class ObstaclesDetectorCommand(ABC):
    @abstractmethod
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> None:
        ...
