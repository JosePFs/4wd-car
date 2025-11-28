from ...domain import ObstaclesDetectorServo
from ..lib.servo import Servo as LibServo


class Servo(ObstaclesDetectorServo):
    def __init__(self) -> None:
        super().__init__()
        self.servo = LibServo()
        self._initial_position = {
            '0': 90,
            '1': 90
        }

    def turn_on(self) -> None:
        self._go_to_initial_position()

    def turn_off(self) -> None:
        self._go_to_initial_position()

    def _go_to_initial_position(self) -> None:
        self.up_down(self._initial_position['0'])
        self.left_right(self._initial_position['1'])

    def up_down(self, angle: int) -> None:
        self.servo.set_servo_pwm('0', angle)

    def left_right(self, angle: int) -> None:
        self.servo.set_servo_pwm('1', angle)
