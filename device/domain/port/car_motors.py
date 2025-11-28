from abc import ABC, abstractmethod

from ..vo.speed import Speed


class CarMotors(ABC):

    @abstractmethod
    def slow_down(self, speed: Speed) -> None:
        ...

    @abstractmethod
    def speed_up(self, speed: Speed) -> None:
        ...

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def move_forward(self) -> None:
        ...

    @abstractmethod
    def move_backward(self) -> None:
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
