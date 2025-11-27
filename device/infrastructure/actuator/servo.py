from ...domain import ObstaclesDetectorServo
from ..lib.servo import Servo as LibServo


class Servo(ObstaclesDetectorServo):
    def __init__(self) -> None:
        super().__init__()
        self.servo = LibServo()

    def turn_off(self) -> None:
        self.servo.set_servo_pwm('0', 90)
        self.servo.set_servo_pwm('1', 90)

    def up_down(self, angle: int) -> None:
        self.servo.set_servo_pwm('0', angle)

    def left_right(self, angle: int) -> None:
        self.servo.set_servo_pwm('1', angle)
