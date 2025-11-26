from dataclasses import dataclass
from typing import Optional

from .event import Event
from ..vo.distance import Distance


@dataclass(frozen=True)
class ObstaclesDetectorTurnOnEvent(Event[None]):
    name: str = "obstacles_detector_turn_on"

    def __str__(self) -> str:
        return f"ObstaclesDetectorTurnOnEvent(name={self.name})"


@dataclass(frozen=True)
class ObstaclesDetectorTurnOffEvent(Event[None]):
    name: str = "obstacles_detector_turn_off"

    def __str__(self) -> str:
        return f"ObstaclesDetectorTurnOffEvent(name={self.name})"


@dataclass(frozen=True)
class ObstacleDetectedEvent(Event[Optional[Distance]]):
    name: str = "obstacle_detected"

    def __str__(self) -> str:
        return f"ObstacleDetectedEvent(name={self.name}, payload={self.payload})"
