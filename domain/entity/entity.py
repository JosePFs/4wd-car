from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from domain.event import Event
from domain.exception.entity_exception import EntityIdException
from domain.vo.id import Id


class Entity(ABC):
    def __init__(self, id: Id = Id.generate()):
        self._id = id

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self._id:
            raise EntityIdException(
                f"Entity {self.__class__.__name__} has no id")

    @property
    def id(self) -> Id:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    @abstractmethod
    def __str__(self) -> str:
        ...


T = TypeVar("T", bound=Entity)


class EntityWithEvents(Generic[T]):
    def __init__(self, entity: T):
        self._entity = entity
        self._events: list[Event] = []

    def with_event(self, event: Event) -> 'EntityWithEvents[T]':
        self._events.append(event)
        return self

    def with_events(self, events: list[Event]) -> 'EntityWithEvents[T]':
        self._events.extend(events)
        return self

    def into_parts(self) -> tuple[T, list[Event]]:
        return self._entity, self._events
