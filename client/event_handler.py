from typing import Callable
from event import Event


class EventHandler:
    def __init__(self):
        self.event_type_to_handle_callbacks: dict[
            type[Event], list[Callable[[Event], None]]
        ] = {}

    def add_callback(self, event_type: type[Event], callback: Callable[[Event], None]):
        if event_type not in self.event_type_to_handle_callbacks:
            self.event_type_to_handle_callbacks[event_type] = []
        self.event_type_to_handle_callbacks[event_type].append(callback)

    def handle(self, event: Event):
        if type(event) in self.event_type_to_handle_callbacks:
            for callback in self.event_type_to_handle_callbacks[type(event)]:
                callback(event)
