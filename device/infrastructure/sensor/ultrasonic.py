from ...domain import ObstaclesDetectorDistance, ObstaclesDetectorException
from ..lib.ultrasonic import Ultrasonic as LibUltrasonic


class Ultrasonic(ObstaclesDetectorDistance):
    def __init__(self) -> None:
        self.ultrasonic = LibUltrasonic()
        self._is_on = False

    def turn_on(self) -> None:
        self._is_on = True

    def turn_off(self) -> None:
        self._is_on = False

    def get_distance(self) -> float:
        if not self._is_on:
            raise ObstaclesDetectorException("Ultrasonic is not on")
        return self.ultrasonic.get_distance()
