from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Optional

from ..vo.value_object import ValueObject

T = TypeVar("T")


@dataclass(frozen=True)
class Event(ABC, Generic[T]):
    name: str = ""
    payload: Optional[ValueObject[T]] = field(default=None)

    def __post_init__(self) -> None:
        if not self.name:
            class_name = type(self).__name__.lower()
            object.__setattr__(self, "name", class_name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return False
        return self.name == other.name and self.payload == other.payload

    def __hash__(self) -> int:
        return hash((self.name, self.payload))

    @abstractmethod
    def __str__(self) -> str:
        ...
