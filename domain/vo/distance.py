from .value_object import ValueObject


class Distance(ValueObject[float]):

    @staticmethod
    def from_centimeters(value: float) -> "Distance":
        return Distance(value=value)

    def __str__(self) -> str:
        return f"Distance(value={self.value} cms)"
