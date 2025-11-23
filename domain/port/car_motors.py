from abc import ABC, abstractmethod


class CarMotors(ABC):

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

    def __str__(self) -> str:
        return f"CarMotors(id={self.id})"
