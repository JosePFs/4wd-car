from abc import ABC, abstractmethod


class Leds(ABC):

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def set_green(self) -> None:
        ...

    @abstractmethod
    def set_red(self) -> None:
        ...
