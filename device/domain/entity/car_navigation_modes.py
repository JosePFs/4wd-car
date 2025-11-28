import random
from typing import TYPE_CHECKING

from ..vo.distance import Distance
from ..vo.speed import Speed
from .car_navigation import CarNavigation, CarNavigationType

if TYPE_CHECKING:
    from .car import Car


class NormalNavigation(CarNavigation):
    def __init__(self, car: 'Car') -> None:
        super().__init__(car)

    def forward(self) -> None:
        self.logger.info("[Normal] Moving forward normally")
        self.car.navigate(lambda m: m.move_forward())

    def backward(self) -> None:
        self.logger.info("[Normal] Moving backward")
        self.car.navigate(lambda m: m.move_backward())

    def turn_left(self) -> None:
        self.logger.info("[Normal] Turning left")
        self.car.navigate(lambda m: m.turn_left())

    def turn_right(self) -> None:
        self.logger.info("[Normal] Turning right")
        self.car.navigate(lambda m: m.turn_right())

    def stop(self) -> None:
        self.logger.info("[Normal] Stopping")
        self.car.navigate(lambda m: m.stop())

    def stop_by_obstacle(self, distance: Distance) -> None:
        self.logger.info(
            f"[Normal] Obstacle detected at {distance}cm! Switching to obstacle detected mode")
        self.car.navigation_mode_transition(
            ObstacleDetectedNavigation(self.car))

    def slow_down(self, speed: Speed) -> None:
        self.logger.info("[Normal] Slow down")
        self.car.navigate(lambda m: m.slow_down(speed))

    def speed_up(self, speed: Speed) -> None:
        self.logger.info("[Normal] Speed up")
        self.car.navigate(lambda m: m.speed_up(speed))

    def turn_on(self) -> None:
        self.logger.info("[Normal] It's already on!")

    def turn_off(self) -> None:
        self.logger.info("[Normal] Turning off")
        self.car.navigation_mode_transition(TurnedOffNavigation(self.car))

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.NORMAL


class ObstacleDetectedNavigation(CarNavigation):
    def __init__(self, car: 'Car') -> None:
        super().__init__(car)

    def forward(self) -> None:
        self.logger.info(
            f"[Obstacle Avoidance] Cannot move forward, turning left instead")
        self.turn_left()

    def backward(self) -> None:
        self.logger.info("[Obstacle Avoidance] Moving backward")
        self.car.navigate(lambda m: m.move_backward())

    def turn_left(self) -> None:
        self.logger.info("[Obstacle Avoidance] Turning left to avoid")
        self.car.navigate(lambda m: m.turn_left())

    def turn_right(self) -> None:
        self.logger.info("[Obstacle Avoidance] Turning right to avoid")
        self.car.navigate(lambda m: m.turn_right())

    def stop(self) -> None:
        self.logger.info("[Obstacle Avoidance] Stopping")
        self.car.navigate(lambda m: m.stop())

    def stop_by_obstacle(self, distance: Distance) -> None:
        self.logger.info("[Obstacle Avoidance] Already avoiding!")

    def slow_down(self, speed: Speed) -> None:
        self.logger.info(
            f"[Obstacle Avoidance] Slow down to {speed}")
        self.car.navigate(lambda m: m.slow_down(speed))
        self.car.navigation_mode_transition(NormalNavigation(self.car))

    def speed_up(self, speed: Speed) -> None:
        self.logger.info(
            f"[Obstacle Avoidance] Speed up to {speed}")
        self.car.navigate(lambda m: m.speed_up(speed))
        self.car.navigation_mode_transition(NormalNavigation(self.car))

    def turn_on(self) -> None:
        self.logger.info("[Obstacle Avoidance] It's already on!")

    def turn_off(self) -> None:
        self.logger.info("[Obstacle Avoidance] Turning off")
        self.car.navigation_mode_transition(TurnedOffNavigation(self.car))

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.OBSTACLE_DETECTED


class TurnedOffNavigation(CarNavigation):
    def __init__(self, car: 'Car') -> None:
        super().__init__(car)

    def forward(self) -> None:
        self.logger.info("[Turned Off] Cannot move forward")

    def backward(self) -> None:
        self.logger.info("[Turned Off] Cannot move backward")

    def turn_left(self) -> None:
        self.logger.info("[Turned Off] Cannot turn left")

    def turn_right(self) -> None:
        self.logger.info("[Turned Off] Cannot turn right")

    def stop(self) -> None:
        self.logger.info("[Turned Off] Cannot stop")

    def stop_by_obstacle(self, distance: Distance) -> None:
        self.logger.info("[Turned Off] Cannot detect obstacles")

    def slow_down(self, speed: Speed) -> None:
        self.logger.info(
            f"[Turned Off] Slow down to {speed}")
        self.car.navigate(lambda m: m.slow_down(speed))

    def speed_up(self, speed: Speed) -> None:
        self.logger.info(
            f"[Turned Off] Speed up to {speed}")
        self.car.navigate(lambda m: m.speed_up(speed))

    def turn_on(self) -> None:
        self.logger.info("[Turned Off] Turning on")
        self.car.navigation_mode_transition(NormalNavigation(self.car))

    def turn_off(self) -> None:
        self.logger.info("[Turned Off] It's already off!")

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.TURNED_OFF


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

    def stop_by_obstacle(self, distance: Distance) -> None:
        self._emergency_stop()

    def _emergency_stop(self) -> None:
        self.logger.info("[Emergency Stop] Emergency stop")
        self.car.navigate(lambda m: m.stop())

    def slow_down(self, speed: Speed) -> None:
        self.logger.info("[Emergency Stop] Cannot slow down")

    def speed_up(self, speed: Speed) -> None:
        self.logger.info("[Emergency Stop] Cannot speed up")

    def turn_on(self) -> None:
        self.logger.info("[Emergency Stop] Turning on")
        self.car.navigation_mode_transition(NormalNavigation(self.car))

    def turn_off(self) -> None:
        self.logger.info("[Emergency Stop] Turning off")
        self.car.navigation_mode_transition(TurnedOffNavigation(self.car))

    def get_type(self) -> CarNavigationType:
        return CarNavigationType.EMERGENCY_STOP
