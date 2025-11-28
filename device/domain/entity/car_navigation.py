from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING
import logging
from logging import Logger

from ..vo.distance import Distance
from ..vo.speed import Speed

if TYPE_CHECKING:
    from .car import Car


class CarNavigationType(Enum):
    NORMAL = "normal"
    OBSTACLE_DETECTED = "obstacle_detected"
    EMERGENCY_STOP = "emergency_stop"
    TURNED_OFF = "turned_off"


class CarNavigation(ABC):
    logger: Logger = logging.getLogger(__name__)

    def __init__(self, car: 'Car') -> None:
        self.car = car

    def emergency_stop(self) -> None:
        from .car_navigation_modes import EmergencyStopNavigation

        self.car.navigate(lambda m: m.stop())
        self.car.navigation_mode_transition(EmergencyStopNavigation(self.car))

    @abstractmethod
    def forward(self) -> None:
        ...

    @abstractmethod
    def backward(self) -> None:
        ...

    @abstractmethod
    def turn_left(self) -> None:
        ...

    @abstractmethod
    def turn_right(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...

    @abstractmethod
    def stop_by_obstacle(self, distance: Distance) -> None:
        ...

    @abstractmethod
    def slow_down(self, speed: Speed) -> None:
        ...

    @abstractmethod
    def speed_up(self, speed: Speed) -> None:
        ...

    @abstractmethod
    def turn_on(self) -> None:
        ...

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def get_type(self) -> CarNavigationType:
        ...
