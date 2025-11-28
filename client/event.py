from dataclasses import dataclass
from abc import ABC, abstractmethod
from pynput import keyboard

dataclass(frozen=True)


class Event(ABC):
    name: str

    @abstractmethod
    def __str__(self) -> str:
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(frozen=True)
class UpPressedEvent(Event):
    name: str = "up"

    def __str__(self) -> str:
        return f"UpPressedEvent(name={self.name})"


@dataclass(frozen=True)
class DownPressedEvent(Event):
    name: str = "down"

    def __str__(self) -> str:
        return f"DownPressedEvent(name={self.name})"


@dataclass(frozen=True)
class LeftPressedEvent(Event):
    name: str = "left"

    def __str__(self) -> str:
        return f"LeftPressedEvent(name={self.name})"


@dataclass(frozen=True)
class RightPressedEvent(Event):
    name: str = "right"

    def __str__(self) -> str:
        return f"RightPressedEvent(name={self.name})"


@dataclass(frozen=True)
class ShiftLeftPressedEvent(Event):
    name: str = "shift_left"

    def __str__(self) -> str:
        return f"ShiftLeftPressedEvent(name={self.name})"


@dataclass(frozen=True)
class ShiftRightPressedEvent(Event):
    name: str = "shift_right"

    def __str__(self) -> str:
        return f"ShiftRightPressedEvent(name={self.name})"

@dataclass(frozen=True)
class KeyReleasedEvent(Event):
    key: keyboard.Key | keyboard.KeyCode
    name: str = "key_released"

    def __str__(self) -> str:
        return f"KeyReleasedEvent(name={self.name}, key={self.key})"