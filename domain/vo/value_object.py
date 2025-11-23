from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ValueObject(ABC, Generic[T]):
    value: T

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError(f"ValueObject must have a value")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    @abstractmethod
    def __str__(self) -> str:
        ...
