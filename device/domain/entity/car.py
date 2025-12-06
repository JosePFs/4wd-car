import logging
from logging import Logger
from typing import Callable

from .autonomous_pilot import AutonomousPilot
from .entity import Entity, EntityWithEvents
from ..vo.distance import Distance
from ..vo.speed import Speed
from .car_navigation import CarNavigation
from ..port import Leds, Buzzer, CarMotors
from .car_navigation_modes import TurnedOffNavigation
from ..event import AutonomousPilotDisabledEvent, AutonomousPilotEnabledEvent, AutonomousPilotExecutedEvent, CarTurnOnEvent, CarTurnOffEvent, CarForwardEvent, CarBackwardEvent, CarTurnLeftEvent, CarTurnRightEvent, CarStopEvent, CarEmergencyStopEvent, CarSlowDownEvent, CarShutdownEvent, CarSpeedUpEvent


class Car(Entity):
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, motors: CarMotors, leds: Leds, buzzer: Buzzer, critical_distance: Distance = Distance.from_centimeters(50), default_speed: Speed = Speed.default(), slow_down_speed: Speed = Speed.from_percentage(60), autonomous_pilot: AutonomousPilot = AutonomousPilot()) -> None:
        super().__init__()
        self.navigation: CarNavigation = TurnedOffNavigation(self)
        self.motors: CarMotors = motors
        self.leds: Leds = leds
        self.buzzer: Buzzer = buzzer
        self.min_distance: Distance = critical_distance
        self.default_speed: Speed = default_speed
        self.slow_down_speed: Speed = slow_down_speed
        self._autonomous_pilot: AutonomousPilot = autonomous_pilot
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

    @property
    def autonomous_pilot_is_enabled(self) -> bool:
        return self._autonomous_pilot.is_enabled

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

    def speed_up(self) -> EntityWithEvents['Car']:
        self.navigation.speed_up(self.default_speed)
        return EntityWithEvents['Car'](self).with_event(CarSpeedUpEvent())

    def navigate(self, action: Callable[[CarMotors], None]) -> None:
        action(self.motors)

    def navigation_mode_transition(self, new_navigation_mode: CarNavigation) -> None:
        self._logger.info(
            f"\n🔄 Navigation mode transition: {self.navigation.get_type().value} -> {new_navigation_mode.get_type().value}")
        self.navigation = new_navigation_mode


    def enable_autonomous_pilot(self) -> EntityWithEvents['Car']:
        self._autonomous_pilot.enable()
        return EntityWithEvents['Car'](self).with_event(AutonomousPilotEnabledEvent())

    def disable_autonomous_pilot(self) -> EntityWithEvents['Car']:
        self._autonomous_pilot.disable()
        return EntityWithEvents['Car'](self).with_event(AutonomousPilotDisabledEvent())

    def execute_autonomous_pilot(self) -> EntityWithEvents['Car']:
        self._autonomous_pilot.drive(self)
        return EntityWithEvents['Car'](self).with_event(AutonomousPilotExecutedEvent())

    def shutdown(self) -> EntityWithEvents['Car']:
        self.navigation.stop()
        self.motors.turn_off()
        self.leds.turn_off()
        self.buzzer.turn_off()
        return EntityWithEvents['Car'](self).with_event(CarShutdownEvent())

    def __str__(self) -> str:
        return f"Car(id={self.id})"
