from abc import ABC, abstractmethod


class Buzzer(ABC):

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def sound_warning(self) -> None:
        ...

    @abstractmethod
    def sound_alarm(self) -> None:
        ...

    @abstractmethod
    def silence(self) -> None:
        ...
