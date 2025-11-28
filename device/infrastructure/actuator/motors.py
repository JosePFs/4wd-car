from ...domain import CarMotors, Speed
from ..lib.motor import Ordinary_Car as LibMotor


class Motors(CarMotors):

    def __init__(self) -> None:
        super().__init__()
        self.motors = LibMotor()
        self.forward_speed: Speed = Speed.default()
        self.backward_speed: Speed = Speed.default()
        self.turn_left_speed: Speed = Speed.default()
        self.turn_right_speed: Speed = Speed.default()
        self.stop_speed: int = 0

    def slow_down(self, speed: Speed) -> None:
        self.forward_speed = speed

    def speed_up(self, speed: Speed) -> None:
        self.forward_speed = speed

    def turn_off(self) -> None:
        self.motors.close()

    def move_forward(self) -> None:
        self.motors.set_motor_model(
            self.forward_speed.value, self.forward_speed.value, self.forward_speed.value, self.forward_speed.value)

    def move_backward(self) -> None:
        self.motors.set_motor_model(-self.backward_speed.value, -
                                    self.backward_speed.value, -self.backward_speed.value, -self.backward_speed.value)

    def turn_left(self) -> None:
        self.motors.set_motor_model(-self.turn_left_speed.value, -self.turn_left_speed.value,
                                    self.turn_left_speed.value * 2, self.turn_left_speed.value * 2)

    def turn_right(self) -> None:
        self.motors.set_motor_model(
            self.turn_right_speed.value * 2, self.turn_right_speed.value * 2, -self.turn_right_speed.value, -self.turn_right_speed.value)

    def stop(self) -> None:
        self.motors.set_motor_model(
            self.stop_speed, self.stop_speed, self.stop_speed, self.stop_speed)
