from queue import Queue
from threading import Thread

from .event import Event


class EventBus:
    def __init__(self):
        self._queue: Queue[Event] = Queue()
        self._handlers: dict[type, list] = {}
        self._running = False

    def start(self):
        self._running = True
        self._thread = Thread(target=self._process_events, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def subscribe(self, event_type: type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: Event):
        self._queue.put(event)

    def publish_all(self, events: list[Event]):
        for event in events:
            self.publish(event)

    def _process_events(self):
        while self._running:
            try:
                event = self._queue.get(timeout=0.1)
                self._dispatch(event)
                self._queue.task_done()
            except Exception:
                continue

    def _dispatch(self, event: Event):
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)
