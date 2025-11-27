import logging
from logging import Logger
from queue import Queue

from ..domain import Car, ObstaclesDetector, EventBus, ObstacleDetectedEvent, DomainException
from .commands import CarCommand, ObstaclesDetectorCommand
from .car_commands_handler import CarCommandsHandler
from .obstacle_detector_commands_handler import ObstaclesDetectorCommandsHandler
from .car_commands import CarAvoidObstacleCommand, CarMoveForwardCommand, CarMoveBackwardCommand, CarTurnLeftCommand, CarTurnRightCommand, CarStopCommand, CarEmergencyStopCommand, CarToggleOnOffCommand
from .obstacles_detector_commands import ObstaclesDetectorToggleOnOffCommand, ObstaclesDetectorDetectCommand


class Application:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, car: Car, obstacles_detector: ObstaclesDetector) -> None:
        self.car = car
        self.obstacles_detector = obstacles_detector

        self.car_commands: Queue[CarCommand] = Queue()
        self.obstacles_commands: Queue[ObstaclesDetectorCommand] = Queue()

        self._event_bus = EventBus()

        self._car_commands_handler = CarCommandsHandler(
            car, self.car_commands, self._event_bus)
        self._obstacles_commands_handler = ObstaclesDetectorCommandsHandler(
            obstacles_detector, self.obstacles_commands, self._event_bus)

        self._event_bus.subscribe(
            ObstacleDetectedEvent, lambda event: self._queue_car_command(CarAvoidObstacleCommand(event.payload)))

    def start(self) -> None:
        try:
            self._event_bus.start()
            self._car_commands_handler.start()
            self._obstacles_commands_handler.start()

        except DomainException as e:
            self._logger.error(f"Error running application: {e}")
            self.stop()
            raise e

    def stop(self) -> None:
        self._event_bus.stop()
        self._car_commands_handler.stop()
        self._obstacles_commands_handler.stop()

    def car_move_forward(self) -> None:
        self._queue_car_command(CarMoveForwardCommand())

    def car_move_backward(self) -> None:
        self._queue_car_command(CarMoveBackwardCommand())

    def car_turn_left(self) -> None:
        self._queue_car_command(CarTurnLeftCommand())

    def car_turn_right(self) -> None:
        self._queue_car_command(CarTurnRightCommand())

    def car_stop(self) -> None:
        self._queue_car_command(CarStopCommand())

    def car_toggle_on_off(self) -> None:
        self._queue_car_command(CarToggleOnOffCommand())

    def obstacles_detector_toggle_on_off(self) -> None:
        self._queue_obstacles_detector_command(
            ObstaclesDetectorToggleOnOffCommand())

    def obstacles_detector_detect(self) -> None:
        self._queue_obstacles_detector_command(
            ObstaclesDetectorDetectCommand())

    def _queue_car_command(self, cmd: CarCommand) -> None:
        self.car_commands.put(cmd)

    def _queue_obstacles_detector_command(self, cmd: ObstaclesDetectorCommand) -> None:
        self.obstacles_commands.put(cmd)
