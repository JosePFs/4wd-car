from typing import Callable, Optional
from event import Event
import logging
from logging import Logger


class EventHandler:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self):
        self.event_type_to_handle_callbacks: dict[
            type[Event], list[tuple[Optional[type[Event]], Callable[[Event], None]]]
        ] = {}
        self.last_parent_event_type: Optional[type[Event]] = None

    def add_callback(
        self,
        parent_event_type: Optional[type[Event]],
        event_type: type[Event],
        callback: Callable[[Event], None],
    ):
        if event_type not in self.event_type_to_handle_callbacks:
            self.event_type_to_handle_callbacks[event_type] = []
        self.event_type_to_handle_callbacks[event_type].append(
            (parent_event_type, callback)
        )

    def handle(self, event: Event):
        if type(event) in self.event_type_to_handle_callbacks:
            for parent_event_type, callback in self.event_type_to_handle_callbacks[
                type(event)
            ]:
                if parent_event_type is None:
                    self.last_parent_event_type = type(event)
                elif parent_event_type != self.last_parent_event_type:
                    continue
                callback(event)
