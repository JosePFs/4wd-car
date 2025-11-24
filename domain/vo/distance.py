from .value_object import ValueObject
from ..exception.value_object_exception import InvalidValueException


class Distance(ValueObject[float]):
    MIN_VALUE = 0
    MAX_VALUE = 1000

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if self.value < self.MIN_VALUE or self.value > self.MAX_VALUE:
            raise InvalidValueException(f"Distance {self.value} is not valid")

    @staticmethod
    def from_centimeters(value: float) -> "Distance":
        return Distance(value=value)

    def __str__(self) -> str:
        return f"Distance(value={self.value} cms)"
