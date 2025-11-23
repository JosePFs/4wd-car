from typing import Generic, TypeVar
from abc import ABC, abstractmethod
import uuid

from domain.event import Event


class Entity(ABC):
    def __init__(self, id: str = uuid.uuid4()):
        self._id = id

    @property
    def id(self) -> str:
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
