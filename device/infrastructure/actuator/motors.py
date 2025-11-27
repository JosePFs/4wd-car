from ...domain import CarMotors, Speed
from ..lib.motor import Ordinary_Car as LibMotor


class Motors(CarMotors):

    def __init__(self) -> None:
        super().__init__()
        self.motors = LibMotor()
        self.speed: Speed = Speed.from_rpm(1000)

    def slow_down(self, speed: Speed) -> None:
        self.speed = speed

    def turn_off(self) -> None:
        self.motors.close()

    def move_forward(self) -> None:
        self.motors.set_motor_model(
            self.speed.value, self.speed.value, self.speed.value, self.speed.value)

    def move_backward(self) -> None:
        self.motors.set_motor_model(-self.speed.value, -
                                    self.speed.value, -self.speed.value, -self.speed.value)

    def turn_left(self) -> None:
        self.motors.set_motor_model(-self.speed.value, -self.speed.value,
                                    self.speed.value * 2, self.speed.value * 2)

    def turn_right(self) -> None:
        self.motors.set_motor_model(
            self.speed.value * 2, self.speed.value * 2, -self.speed.value, -self.speed.value)

    def stop(self) -> None:
        self.motors.set_motor_model(0, 0, 0, 0)
