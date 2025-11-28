from enum import Enum

class CommandType(Enum):
    CONTINOUS = "continous"
    DISCRETE = "discrete"

class Command(Enum):
    FORWARD = ("car_forward", CommandType.CONTINOUS)
    BACKWARD = ("car_backward", CommandType.CONTINOUS)
    LEFT = ("car_left", CommandType.CONTINOUS)
    RIGHT = ("car_right", CommandType.CONTINOUS)
    STOP = ("car_stop", CommandType.DISCRETE)
    TOGGLE_CAR_ON_OFF = ("car_toggle_on_off", CommandType.DISCRETE)
    TOGGLE_OBSTACLE_DETECTION_ON_OFF = ("obstacles_detector_toggle_on_off", CommandType.DISCRETE)

    @property
    def continous(self) -> bool:
        return self.value[1] == CommandType.CONTINOUS

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

    def __str__(self) -> str:
        return self.name