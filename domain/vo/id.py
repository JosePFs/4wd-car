from uuid import uuid4

from .value_object import ValueObject
from ..exception.entity_exception import EntityIdException


class Id(ValueObject[str]):
    def __init__(self, value: str):
        super().__init__(value)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.value:
            raise EntityIdException(f"Id {self.value} is not valid")

    @staticmethod
    def generate() -> "Id":
        return Id(value=str(uuid4()))

    def __str__(self) -> str:
        return f"Id(value={self.value})"
