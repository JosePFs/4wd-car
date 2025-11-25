from dataclasses import dataclass
from abc import ABC, abstractmethod

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
class SpacePressedEvent(Event):
    name: str = "space"

    def __str__(self) -> str:
        return f"SpacePressedEvent(name={self.name})"

@dataclass(frozen=True)
class ShiftPressedEvent(Event):
    name: str = "ctrl"

    def __str__(self) -> str:
        return f"CtrlPressedEvent(name={self.name})"

@dataclass(frozen=True)
class EscapePressedEvent(Event):
    name: str = "escape"

    def __str__(self) -> str:
        return f"EscapePressedEvent(name={self.name})"