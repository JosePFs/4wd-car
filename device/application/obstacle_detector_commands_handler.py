from queue import Queue, Empty
from threading import Thread, Event
import logging
from logging import Logger

from ..domain import ObstaclesDetector, EventBus, ObstaclesDetectorException, UnhandledException
from .commands import ObstaclesDetectorCommand


class ObstaclesDetectorCommandsHandler(Thread):
    _logger: Logger = logging.getLogger(__name__)

    def __init__(
        self,
        obstacles_detector: ObstaclesDetector,
        command_queue: Queue[ObstaclesDetectorCommand],
        event_bus: EventBus,
    ):
        super().__init__(daemon=False)
        self._obstacles_detector = obstacles_detector
        self._command_queue = command_queue
        self._event_bus = event_bus

        self._stop_event = Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                command = self._command_queue.get(timeout=0.1)
                result = command.execute(self._obstacles_detector)
                self._event_bus.publish_all(result.events)
                self._command_queue.task_done()

            except Empty:
                continue
            except ObstaclesDetectorException as e:
                self._logger.error(f"Obstacles detector exception: {e}")
                self._stop_obstacles_detector()
                raise e
            except Exception as e:
                self._logger.error(
                    f"Error executing obstacles detector command: {e}")
                self._stop_obstacles_detector()
                raise UnhandledException() from e

        if self._obstacles_detector.is_on:
            self._obstacles_detector.turn_off()

    def _stop_obstacles_detector(self) -> None:
        if self._obstacles_detector.is_on:
            self._obstacles_detector.turn_off()

    def stop(self) -> None:
        self._stop_event.set()
        self.join()
