from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .car import Car


class CarNavigationType(Enum):
    NORMAL = "normal"
    OBSTACLE_DETECTED = "obstacle_detected"
    EMERGENCY_STOP = "emergency_stop"


class CarNavigation(ABC):
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
    def obstacle_detected(self, distance: float) -> None:
        ...

    @abstractmethod
    def get_type(self) -> CarNavigationType:
        ...
