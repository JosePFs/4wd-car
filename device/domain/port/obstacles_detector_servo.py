from abc import ABC, abstractmethod


class ObstaclesDetectorServo(ABC):

    @abstractmethod
    def turn_on(self) -> None:
        ...

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def up_down(self, angle: int) -> None:
        ...

    @abstractmethod
    def left_right(self, angle: int) -> None:
        ...
