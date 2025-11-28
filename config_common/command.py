from enum import Enum
from typing import Optional
from dataclasses import dataclass

class Command(Enum):
    FORWARD = ("car_forward", None)
    BACKWARD = ("car_backward", None)
    LEFT = ("car_left", None)
    RIGHT = ("car_right", None)
    STOP = ("car_stop", str)
    TOGGLE_CAR_ON_OFF = ("car_toggle_on_off", None)
    TOGGLE_OBSTACLE_DETECTION_ON_OFF = ("obstacles_detector_toggle_on_off", None)

    def with_key(self, key: str) -> "CommandWithKey":
        if self.value[1] is not None:
            return CommandWithKey(self, key)
        return CommandWithKey(self, None)

    @classmethod
    def from_string(cls, string: str) -> "Command":
        normalized = string.strip().upper()
        
        try:
            return cls[normalized]
        except KeyError:
            pass
            
        try:
            return cls(string.strip().lower())
        except ValueError:
            raise ValueError(f"'{string}' is not a valid Command")

@dataclass(frozen=True)
class CommandWithKey:
    command: Command
    key: Optional[str]

    def __str__(self) -> str:
        return f"{self.command.name} {self.key}"