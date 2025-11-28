import logging
from logging import Logger
from typing import Callable

from .entity import Entity, EntityWithEvents
from ..vo.distance import Distance
from ..vo.speed import Speed
from .car_navigation import CarNavigation
from ..port import Leds, Buzzer, CarMotors
from .car_navigation_modes import TurnedOffNavigation
from ..event import CarTurnOnEvent, CarTurnOffEvent, CarForwardEvent, CarBackwardEvent, CarTurnLeftEvent, CarTurnRightEvent, CarStopEvent, CarEmergencyStopEvent, CarSlowDownEvent, CarShutdownEvent, CarStoppedByObstacleEvent, CarSpeedUpEvent


class Car(Entity):
    logger: Logger = logging.getLogger(__name__)

    def __init__(self, motors: CarMotors, leds: Leds, buzzer: Buzzer, critical_distance: Distance = Distance.from_centimeters(50), default_speed: Speed = Speed.default(), slow_down_speed: Speed = Speed.from_percentage(60)) -> None:
        super().__init__()
        self.navigation: CarNavigation = TurnedOffNavigation(self)
        self.motors: CarMotors = motors
        self.leds: Leds = leds
        self.buzzer: Buzzer = buzzer
        self.min_distance: Distance = critical_distance
        self.default_speed: Speed = default_speed
        self.slow_down_speed: Speed = slow_down_speed
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def critical_distance(self) -> Distance:
        return Distance.from_centimeters(self.min_distance.value)

    @property
    def safe_distance(self) -> Distance:
        return Distance.from_centimeters(self.min_distance.value * 2)

    def turn_on(self) -> EntityWithEvents['Car']:
        self._is_on = True
        self.navigation.turn_on()
        return EntityWithEvents['Car'](self).with_event(CarTurnOnEvent())

    def turn_off(self) -> EntityWithEvents['Car']:
        self._is_on = False
        self.navigation.turn_off()
        return EntityWithEvents['Car'](self).with_event(CarTurnOffEvent())

    def forward(self) -> EntityWithEvents['Car']:
        self.navigation.forward()
        return EntityWithEvents['Car'](self).with_event(CarForwardEvent())

    def backward(self) -> EntityWithEvents['Car']:
        self.navigation.backward()
        return EntityWithEvents['Car'](self).with_event(CarBackwardEvent())

    def turn_left(self) -> EntityWithEvents['Car']:
        self.navigation.turn_left()
        return EntityWithEvents['Car'](self).with_event(CarTurnLeftEvent())

    def turn_right(self) -> EntityWithEvents['Car']:
        self.navigation.turn_right()
        return EntityWithEvents['Car'](self).with_event(CarTurnRightEvent())

    def stop(self) -> EntityWithEvents['Car']:
        self.navigation.stop()
        return EntityWithEvents['Car'](self).with_event(CarStopEvent())

    def emergency_stop(self) -> EntityWithEvents['Car']:
        self.navigation.emergency_stop()
        return EntityWithEvents['Car'](self).with_event(CarEmergencyStopEvent())

    def slow_down(self) -> EntityWithEvents['Car']:
        self.navigation.slow_down(self.slow_down_speed)
        return EntityWithEvents['Car'](self).with_event(CarSlowDownEvent())

    def stop_by_obstacle(self, distance: Distance) -> EntityWithEvents['Car']:
        self.navigation.stop_by_obstacle(distance)
        return EntityWithEvents['Car'](self).with_event(CarStoppedByObstacleEvent(payload=distance))

    def speed_up(self) -> EntityWithEvents['Car']:
        self.navigation.speed_up(self.default_speed)
        return EntityWithEvents['Car'](self).with_event(CarSpeedUpEvent())

    def navigate(self, action: Callable[[CarMotors], None]) -> None:
        action(self.motors)

    def navigation_mode_transition(self, new_navigation_mode: CarNavigation) -> None:
        self.logger.info(
            f"\n🔄 Navigation mode transition: {self.navigation.get_type().value} -> {new_navigation_mode.get_type().value}")
        self.navigation = new_navigation_mode

    def shutdown(self) -> EntityWithEvents['Car']:
        self.navigation.stop()
        self.motors.turn_off()
        self.leds.turn_off()
        self.buzzer.turn_off()
        return EntityWithEvents['Car'](self).with_event(CarShutdownEvent())

    def __str__(self) -> str:
        return f"Car(id={self.id})"
