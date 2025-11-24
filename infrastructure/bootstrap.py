import logging
from logging import Logger
from queue import Queue

from domain import Car, ObstaclesDetector, EventBus, ObstacleDetectedEvent, DomainException
from application import CarCommand, ObstaclesDetectorCommand, CarAvoidObstacleCommand, CarCommandsHandler, ObstaclesDetectorCommandsHandler
from infrastructure import Motors, Leds, Buzzer, Ultrasonic, Servo


class Application:
    logger: Logger = logging.getLogger(__name__)

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
            ObstacleDetectedEvent, lambda event: self.queue_car_command(CarAvoidObstacleCommand(event.payload)))

    def run(self) -> None:
        try:
            self._event_bus.start()
            self._car_commands_handler.start()
            self._obstacles_commands_handler.start()

        except DomainException as e:
            self.logger.error(f"Error running application: {e}")
            self._event_bus.stop()
            self._car_commands_handler.stop()
            self._obstacles_commands_handler.stop()
            raise e

    def queue_car_command(self, cmd: CarCommand) -> None:
        self.car_commands.put(cmd)

    def queue_obstacles_detector_command(self, cmd: ObstaclesDetectorCommand) -> None:
        self.obstacles_commands.put(cmd)


def build_application() -> Application:
    motors = Motors()
    leds = Leds()
    buzzer = Buzzer()
    car = Car(motors, leds, buzzer)
    obstacles_detector = ObstaclesDetector(Ultrasonic(), Servo())
    return Application(car, obstacles_detector)
