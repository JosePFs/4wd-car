from queue import Queue, Empty
from threading import Thread
import logging
from logging import Logger

from domain import Car, EventBus, CarException
from .commands import CarCommand


class CarCommandsHandler(Thread):
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, car: Car, command_queue: Queue[CarCommand], event_bus: EventBus):
        super().__init__(daemon=False)
        self._car = car
        self._command_queue = command_queue
        self._event_bus = event_bus

    def run(self):
        self._car.turn_on()

        while self._car.is_on:
            try:
                command = self._command_queue.get(timeout=0.1)

                result = command.execute(self._car)

                self._event_bus.publish_all(result.events)

                self._command_queue.task_done()

            except Empty:
                continue
            except CarException as e:
                self._logger.error(f"Car exception: {e}")
                raise e
            except Exception as e:
                self._logger.error(f"Error executing car command: {e}")
                raise e

    def stop(self):
        self._car.turn_off()
        self.join()
