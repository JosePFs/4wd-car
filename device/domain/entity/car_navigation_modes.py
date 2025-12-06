from typing import TYPE_CHECKING

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
