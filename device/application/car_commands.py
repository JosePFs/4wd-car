from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
import logging
from logging import Logger

from .commands import CarCommand, CommandResult
from ..domain import Distance


if TYPE_CHECKING:
    from domain import Car


class CarToggleOnOffCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        if car.is_on:
            _, events = car.turn_off().into_parts()
        else:
            _, events = car.turn_on().into_parts()
        return CommandResult(events=events)


class CarMoveForwardCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        car_entity, events = car.forward().into_parts()
        return CommandResult(events=events)


class CarMoveBackwardCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        _, events = car.backward().into_parts()
        return CommandResult(events=events)


class CarTurnLeftCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        _, events = car.turn_left().into_parts()
        return CommandResult(events=events)


class CarTurnRightCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        _, events = car.turn_right().into_parts()
        return CommandResult(events=events)


class CarStopCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        _, events = car.stop().into_parts()
        return CommandResult(events=events)


class CarEmergencyStopCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        _, events = car.emergency_stop().into_parts()
        return CommandResult(events=events)


@dataclass(frozen=True)
class CarAvoidObstacleCommand(CarCommand):
    distance: Distance

    _logger: ClassVar[Logger] = logging.getLogger(__name__)

    def execute(self, car: 'Car') -> CommandResult:
        self._logger.info(
            f"🔍 CarAvoidObstacleCommand: distance={self.distance}")
        if self.distance.value < car.critical_distance.value:
            _, events = car.stop_by_obstacle(self.distance).into_parts()
        elif self.distance.value < car.safe_distance.value:
            _, events = car.slow_down().into_parts()
        else:
            _, events = car.speed_up().into_parts()
        return CommandResult(events=events)
