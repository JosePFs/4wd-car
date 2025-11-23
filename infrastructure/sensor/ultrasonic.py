from domain import ObstaclesDetectorDistance
from infrastructure.lib.ultrasonic import Ultrasonic as LibUltrasonic


class Ultrasonic(ObstaclesDetectorDistance):
    def __init__(self) -> None:
        self.ultrasonic = LibUltrasonic()

    def turn_off(self) -> None:
        self.ultrasonic.close()

    def get_distance(self) -> float:
        return self.ultrasonic.get_distance()
