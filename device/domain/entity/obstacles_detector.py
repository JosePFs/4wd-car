import logging
from logging import Logger

from .entity import Entity
from ..port import ObstaclesDetectorDistance, ObstaclesDetectorServo
from .entity import EntityWithEvents
from ..event import ObstaclesDetectorTurnOnEvent, ObstaclesDetectorTurnOffEvent, ObstacleDetectedEvent
from ..vo.distance import Distance


class ObstaclesDetector(Entity):
    logger: Logger = logging.getLogger(__name__)

    def __init__(self, distance_detector: ObstaclesDetectorDistance, servo: ObstaclesDetectorServo) -> None:
        super().__init__()
        self.distance_detector: ObstaclesDetectorDistance = distance_detector
        self.servo: ObstaclesDetectorServo = servo

        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    def turn_on(self) -> EntityWithEvents['ObstaclesDetector']:
        self._is_on = True
        return EntityWithEvents['ObstaclesDetector'](self).with_event(ObstaclesDetectorTurnOnEvent())

    def turn_off(self) -> EntityWithEvents['ObstaclesDetector']:
        self._is_on = False
        self.servo.turn_off()
        self.distance_detector.turn_off()
        return EntityWithEvents['ObstaclesDetector'](self).with_event(ObstaclesDetectorTurnOffEvent())

    def detect(self) -> EntityWithEvents['ObstaclesDetector']:
        distance = Distance.from_centimeters(
            self.distance_detector.get_distance())
        self.logger.info(f"🔍 Obstacles detector: {distance}")
        return EntityWithEvents['ObstaclesDetector'](self).with_event(ObstacleDetectedEvent(payload=distance))

    def __str__(self) -> str:
        return f"ObstaclesDetector(id={self.id})"
