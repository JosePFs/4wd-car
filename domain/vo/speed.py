from .value_object import ValueObject


class Speed(ValueObject[int]):
    @staticmethod
    def from_rpm(value: int) -> "Speed":
        return Speed(value=value)

    @staticmethod
    def from_percentage(value: float) -> "Speed":
        return Speed(value=int(value * 10))

    def __str__(self) -> str:
        return f"Speed(value={self.value} rpm)"
