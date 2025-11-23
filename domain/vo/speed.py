from .value_object import ValueObject


class Speed(ValueObject[int]):
    @staticmethod
    def from_rpm(value: int) -> "Speed":
        return Speed(value=value)

    def __str__(self) -> str:
        return f"Speed(value={self.value})"
