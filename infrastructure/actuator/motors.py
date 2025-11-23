from domain import CarMotors
from infrastructure.lib.motor import Ordinary_Car as LibMotor


class Motors(CarMotors):

    def __init__(self) -> None:
        super().__init__()
        self.motors = LibMotor()

    def turn_off(self) -> None:
        self.motors.close()

    def move_forward(self) -> None:
        self.motors.set_motor_model(1000, 1000, 1000, 1000)

    def move_backward(self) -> None:
        self.motors.set_motor_model(-1000, -1000, -1000, -1000)

    def turn_left(self) -> None:
        self.motors.set_motor_model(-1000, -1000, 2000, 2000)

    def turn_right(self) -> None:
        self.motors.set_motor_model(2000, 2000, -1000, -1000)

    def stop(self) -> None:
        self.motors.set_motor_model(0, 0, 0, 0)
