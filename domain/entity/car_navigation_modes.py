import random
from typing import TYPE_CHECKING

from .car_navigation import CarNavigation, CarNavigationType

if TYPE_CHECKING:
    from .car import Car


class NormalNavigation(CarNavigation):
    def __init__(self, car: 'Car') -> None:
        super().__init__(car)

    def forward(self) -> None:
        print("[Normal] Moving forward normally")
        self.car.navigate(lambda m: m.move_forward())

    def backward(self) -> None:
        print("[Normal] Moving backward")
        self.car.navigate(lambda m: m.move_backward())

    def turn_left(self) -> None:
        print("[Normal] Turning left")
        self.car.navigate(lambda m: m.turn_left())

    def turn_right(self) -> None:
        print("[Normal] Turning right")
        self.car.navigate(lambda m: m.turn_right())

    def stop(self) -> None:
        print("[Normal] Stopping")
        self.car.navigate(lambda m: m.stop())

    def obstacle_detected(self, distance: float) -> None:
        print(
            f"[Normal] Obstacle detected at {distance}cm! Switching to obstacle detected mode")
        self.stop()
        self.car.navigation_mode_transition(
            ObstacleDetectedNavigation(self.car))

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.NORMAL


class ObstacleDetectedNavigation(CarNavigation):
    def __init__(self, car: 'Car') -> None:
        super().__init__(car)

    def forward(self) -> None:
        direction = random.choice(["left", "right"])
        print(
            f"[Obstacle Avoidance] Cannot move forward, turning {direction} instead")
        if direction == "left":
            self.turn_left()
        else:
            self.turn_right()
        self.car.navigation_mode_transition(NormalNavigation(self.car))

    def backward(self) -> None:
        print("[Obstacle Avoidance] Moving backward")
        self.car.navigate(lambda m: m.move_backward())

    def turn_left(self) -> None:
        print("[Obstacle Avoidance] Turning left to avoid")
        self.car.navigate(lambda m: m.turn_left())

    def turn_right(self) -> None:
        print("[Obstacle Avoidance] Turning right to avoid")
        self.car.navigate(lambda m: m.turn_right())

    def stop(self) -> None:
        print("[Obstacle Avoidance] Stopping")
        self.car.navigate(lambda m: m.stop())

    def obstacle_detected(self, distance: float) -> None:
        print("[Obstacle Avoidance] Already avoiding!")

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.OBSTACLE_DETECTED


class EmergencyStopNavigation(CarNavigation):
    def __init__(self, car: 'Car') -> None:
        super().__init__(car)

    def forward(self) -> None:
        self._emergency_stop()

    def backward(self) -> None:
        self._emergency_stop()

    def turn_left(self) -> None:
        self._emergency_stop()

    def turn_right(self) -> None:
        self._emergency_stop()

    def stop(self) -> None:
        self._emergency_stop()

    def obstacle_detected(self, distance: float) -> None:
        self._emergency_stop()

    def _emergency_stop(self) -> None:
        print("[Emergency Stop] Emergency stop")
        self.car.navigate(lambda m: m.stop())

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.EMERGENCY_STOP
