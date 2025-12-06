from enum import Enum

from .car import Car
from ..exception import AutonomousPilotException
from .entity import Entity


class AutonomousPilotPauseReason(Enum):
    USER_REQUESTED = "user_requested"
    OBSTACLE_DETECTED = "obstacle_detected"
    EMERGENCY_STOP = "emergency_stop"

class AutonomousPilotState(Enum):
    ACTIVE = "active"
    PAUSED = ("paused", AutonomousPilotPauseReason)

class WallSide(Enum):
    LEFT = "left"
    RIGHT = "right"

class AutonomousPilotNavigationMode(Enum):
    OBSTACLE_AVOIDANCE = "obstacle_avoidance"
    WALL_FOLLOWING = ("wall_following", WallSide)

class AutonomousPilot(Entity):
    def __init__(self, state: AutonomousPilotState = AutonomousPilotState.ACTIVE, navigation_mode: AutonomousPilotNavigationMode = AutonomousPilotNavigationMode.OBSTACLE_AVOIDANCE) -> None:
        super().__init__()
        self._state = state
        self._navigation_mode = navigation_mode

    @property
    def state(self) -> AutonomousPilotState:
        return self._state

    @property
    def navigation_mode(self) -> AutonomousPilotNavigationMode:
        return self._navigation_mode

    @property
    def is_enabled(self) -> bool:
        return self._state == AutonomousPilotState.ACTIVE

    def enable(self) -> None:
        if self._state == AutonomousPilotState.ACTIVE:
            raise AutonomousPilotException("Autonomous pilot is already enabled")
        self._state = AutonomousPilotState.ACTIVE

    def disable(self) -> None:
        if self._state == AutonomousPilotState.PAUSED:
            raise AutonomousPilotException("Autonomous pilot is already disabled")
        self._state = AutonomousPilotState.PAUSED

    def drive(self, car: Car) -> None:
        if self._state == AutonomousPilotState.PAUSED:
            raise AutonomousPilotException("Autonomous pilot is paused")

        match self._navigation_mode:
            case AutonomousPilotNavigationMode.OBSTACLE_AVOIDANCE:
                self._navigate_obstacle_avoidance(car)
            case AutonomousPilotNavigationMode.WALL_FOLLOWING:
                self._navigate_wall_following(car)
    
    def _navigate_obstacle_avoidance(self, car: Car) -> None:
        pass

    def _navigate_wall_following(self, car: Car) -> None:
        pass

    def __str__(self) -> str:
        return f"AutonomousPilot(id={self.id}, state={self.state.value}, navigation_mode={self.navigation_mode.value})"