from .value_object import ValueObject
from ..exception.value_object_exception import InvalidValueException


class Speed(ValueObject[int]):
    MIN_VALUE = 0
    MAX_VALUE = 1000

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if self.value < self.MIN_VALUE or self.value > self.MAX_VALUE:
            raise InvalidValueException(f"Speed {self.value} is not valid")

    @staticmethod
    def from_rpm(value: int) -> "Speed":
        return Speed(value=value)

    @staticmethod
    def from_percentage(value: float) -> "Speed":
        return Speed(value=int(value * 10))

    def __str__(self) -> str:
        return f"Speed(value={self.value} rpm)"
