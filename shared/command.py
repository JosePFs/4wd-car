from dataclasses import dataclass
from enum import Enum


class DriveMode(Enum):
    OBSTANCES_AVOIDANCE = "obstances_avoidance"
    WALLS_FOLLOWING = "walls_following"
    MANUAL = "manual"

    @classmethod
    def from_string(cls, string: str) -> "DriveMode":
        try:
            return cls(string.strip().lower())
        except ValueError:
            raise ValueError(f"'{string}' is not a valid DriveMode")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ActivateMode:
    mode: DriveMode

    def encode(self) -> bytes:
        return f"activate_mode:{self.mode.value}".encode("utf-8")

    def __str__(self) -> str:
        return f"Command(activate_mode:{self.mode.value})"


@dataclass(frozen=True)
class DeactivateMode:
    def encode(self) -> bytes:
        return b"deactivate_mode"

    def __str__(self) -> str:
        return "Command(deactivate_mode)"


@dataclass(frozen=True)
class StopCarImmediately:
    def encode(self) -> bytes:
        return b"stop_car_immediately"

    def __str__(self) -> str:
        return "Command(stop_car_immediately)"


@dataclass(frozen=True)
class ResumeCarMovement:
    def encode(self) -> bytes:
        return b"resume_car_movement"

    def __str__(self) -> str:
        return "Command(resume_car_movement)"


Command = ActivateMode | DeactivateMode | StopCarImmediately | ResumeCarMovement


def parse_command(string: str) -> Command:
    if ":" in string:
        name, args = string.split(":", 1)
    else:
        name, args = string, ""

    match name:
        case "activate_mode":
            return ActivateMode(mode=DriveMode.from_string(args))
        case "deactivate_mode":
            return DeactivateMode()
        case "stop_car_immediately":
            return StopCarImmediately()
        case "resume_car_movement":
            return ResumeCarMovement()
        case _:
            raise ValueError(f"Invalid command: {string}")
