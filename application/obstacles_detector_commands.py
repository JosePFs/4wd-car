from typing import TYPE_CHECKING

from .commands import ObstaclesDetectorCommand, CommandResult

if TYPE_CHECKING:
    from domain import ObstaclesDetector


class ObstaclesDetectorTurnOnCommand(ObstaclesDetectorCommand):
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> CommandResult:
        _, events = obstacles_detector.turn_on().into_parts()
        return CommandResult(events=events)


class ObstaclesDetectorTurnOffCommand(ObstaclesDetectorCommand):
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> CommandResult:
        _, events = obstacles_detector.turn_off().into_parts()
        return CommandResult(events=events)


class ObstaclesDetectorDetectCommand(ObstaclesDetectorCommand):
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> CommandResult:
        _, events = obstacles_detector.detect().into_parts()
        return CommandResult(events=events)
