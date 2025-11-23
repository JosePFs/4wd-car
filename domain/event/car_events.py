from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Optional

from .event import Event


@dataclass(frozen=True)
class CarTurnOffEvent(Event[None]):
    name: str = "car_turn_off"

    def __str__(self) -> str:
        return f"CarTurnOffEvent(name={self.name})"


@dataclass(frozen=True)
class CarForwardEvent(Event[None]):
    name: str = "car_forward"

    def __str__(self) -> str:
        return f"CarForwardEvent(name={self.name})"


@dataclass(frozen=True)
class CarBackwardEvent(Event[None]):
    name: str = "car_backward"

    def __str__(self) -> str:
        return f"CarBackwardEvent(name={self.name})"


@dataclass(frozen=True)
class CarTurnLeftEvent(Event[None]):
    name: str = "car_turn_left"

    def __str__(self) -> str:
        return f"CarTurnLeftEvent(name={self.name})"


@dataclass(frozen=True)
class CarTurnRightEvent(Event[None]):
    name: str = "car_turn_right"

    def __str__(self) -> str:
        return f"CarTurnRightEvent(name={self.name})"


@dataclass(frozen=True)
class CarStopEvent(Event[None]):
    name: str = "car_stop"

    def __str__(self) -> str:
        return f"CarStopEvent(name={self.name})"


@dataclass(frozen=True)
class CarEmergencyStopEvent(Event[None]):
    name: str = "car_emergency_stop"

    def __str__(self) -> str:
        return f"CarEmergencyStopEvent(name={self.name})"
