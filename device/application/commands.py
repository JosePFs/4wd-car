from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain import Car
    from domain import ObstaclesDetector

from domain import Event


@dataclass(frozen=True)
class CommandResult:
    success: bool = True
    events: list[Event] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.success

    def __str__(self) -> str:
        return f"CommandResult(success={self.success}, events={self.events})"


class CarCommand(ABC):
    @abstractmethod
    def execute(self, car: 'Car') -> CommandResult:
        ...


class ObstaclesDetectorCommand(ABC):
    @abstractmethod
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> CommandResult:
        ...
