from queue import Queue, Empty
from threading import Thread, Event
import logging
from logging import Logger

from domain import Car, EventBus, CarException, UnhandledException
from .commands import CarCommand


class CarCommandsHandler(Thread):
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, car: Car, command_queue: Queue[CarCommand], event_bus: EventBus):
        super().__init__(daemon=False)
        self._car = car
        self._command_queue = command_queue
        self._event_bus = event_bus

        self._stop_event = Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                command = self._command_queue.get(timeout=0.1)
                result = command.execute(self._car)
                self._event_bus.publish_all(result.events)
                self._command_queue.task_done()

            except Empty:
                continue
            except CarException as e:
                self._logger.error(f"Car exception: {e}")
                self._stop_car()
                raise e
            except Exception as e:
                self._logger.error(f"Error executing car command: {e}")
                self._stop_car()
                raise UnhandledException() from e

        self._stop_car()

    def _stop_car(self) -> None:
        if self._car.is_on:
            self._car.turn_off()

    def stop(self) -> None:
        self._stop_event.set()
        self.join()
