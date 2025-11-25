from enum import Enum

class Command(Enum):
    FORWARD = "car_forward"
    BACKWARD = "car_backward"
    LEFT = "car_left"
    RIGHT = "car_right"
    STOP = "car_stop"
    TOGGLE_CAR_ON_OFF = "car_toggle_on_off"
    TOGGLE_OBSTACLE_DETECTION_ON_OFF = "obstacles_detector_toggle_on_off"

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