from typing import TYPE_CHECKING

from .commands import ObstaclesDetectorCommand, CommandResult
from ..domain import ObstaclesDetector


class ObstaclesDetectorToggleOnOffCommand(ObstaclesDetectorCommand):
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> CommandResult:
        if obstacles_detector.is_on:
            _, events = obstacles_detector.turn_off().into_parts()
        else:
            _, events = obstacles_detector.turn_on().into_parts()
        return CommandResult(events=events)


class ObstaclesDetectorDetectCommand(ObstaclesDetectorCommand):
    def execute(self, obstacles_detector: 'ObstaclesDetector') -> CommandResult:
        _, events = obstacles_detector.detect().into_parts()
        return CommandResult(events=events)
