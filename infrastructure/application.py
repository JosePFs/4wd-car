import threading
import logging
from logging import Logger
from queue import Queue

from domain import Car, ObstaclesDetector, EventBus, ObstacleDetectedEvent
from application import CarCommand, ObstaclesDetectorCommand, CarTurnOffCommand, ObstaclesDetectorTurnOffCommand
from infrastructure import Motors, Leds, Buzzer, Ultrasonic, Servo


class Application:
    logger: Logger = logging.getLogger(__name__)

    def __init__(self, car: Car, obstacles_detector: ObstaclesDetector) -> None:
        self.car = car
        self.obstacles_detector = obstacles_detector

        self.car_commands: Queue[CarCommand] = Queue()
        self.obstacles_commands: Queue[ObstaclesDetectorCommand] = Queue()

        self._stop_event = threading.Event()
        self._threads: list[threading.Thread] = []
        self._event_bus = EventBus()

        self._event_bus.subscribe(
            ObstacleDetectedEvent, self.car.on_obstacle_detected)

    def start(self) -> None:
        self._threads = [
            threading.Thread(target=self._run_car),
            threading.Thread(target=self._run_obstacles),
        ]
        for thread in self._threads:
            thread.start()

    def _run_car(self) -> None:
        while not self._stop_event.is_set():
            cmd = self.car_commands.get()

            if isinstance(cmd, CarTurnOffCommand):
                self.logger.info("Car shutdown command received")
                result = cmd.execute(self.car)
                if not result.success:
                    self.logger.error("Car shutdown command failed")
                    break
                for event in result.events:
                    self.logger.info(f"Car event: {event}")
                break

            result = cmd.execute(self.car)
            if not result.success:
                self.logger.error("Car command failed")
                break
            for event in result.events:
                self.logger.info(f"Car event: {event}")

    def _run_obstacles(self) -> None:
        while not self._stop_event.is_set():
            cmd = self.obstacles_commands.get()

            if isinstance(cmd, ObstaclesDetectorTurnOffCommand):
                self.logger.info("Obstacle detector shutdown command received")
                result = cmd.execute(self.obstacles_detector)
                if not result.success:
                    self.logger.error(
                        "Obstacle detector shutdown command failed")
                    break
                for event in result.events:
                    self.logger.info(f"Obstacle detector event: {event}")
                break

            result = cmd.execute(self.obstacles_detector)
            if not result.success:
                self.logger.error("Obstacle detector command failed")
                break
            for event in result.events:
                self.logger.info(f"Obstacle detector event: {event}")

    def stop(self) -> None:
        if self._stop_event.is_set():
            return

        self.queue_car_command(CarTurnOffCommand())
        self.queue_obstacles_detector_command(
            ObstaclesDetectorTurnOffCommand())

        for thread in self._threads:
            thread.join()

        self._stop_event.set()

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
