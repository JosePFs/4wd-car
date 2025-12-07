from dataclasses import dataclass
from abc import ABC, abstractmethod
from pynput import keyboard


@dataclass(frozen=True)
class Event(ABC):
    key: keyboard.Key | keyboard.KeyCode

    def __str__(self) -> str:
        return (
            f"Event(key={self.key}, should_send_release={self.should_send_release()})"
        )

    @classmethod
    @abstractmethod
    def should_send_release(cls) -> bool: ...


@dataclass(frozen=True)
class UpPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return True


@dataclass(frozen=True)
class DownPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return True


@dataclass(frozen=True)
class LeftPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return True


@dataclass(frozen=True)
class RightPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return True


@dataclass(frozen=True)
class KeyOnePressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class KeyTwoPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class KeyThreePressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class KeyZeroPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class ShiftLeftPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class ShiftRightPressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class SpacePressedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False


@dataclass(frozen=True)
class KeyReleasedEvent(Event):

    @classmethod
    def should_send_release(cls) -> bool:
        return False
