from dataclasses import dataclass
from typing import TYPE_CHECKING

from .commands import CarCommand
from .command_result import CommandResult
from domain import Distance, Speed


if TYPE_CHECKING:
    from domain import Car


class CarTurnOffCommand(CarCommand):
    def execute(self, car: 'Car') -> CommandResult:
        _, events = car.turn_off().into_parts()
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

    def execute(self, car: 'Car') -> CommandResult:
        if self.distance < car.critical_distance:
            _, events = car.emergency_stop().into_parts()
        elif self.distance < car.safe_distance:
            _, events = car.slow_down(Speed.from_percentage(30)).into_parts()
        else:
            events = []
        return CommandResult(events=events)
