import logging
from logging import Logger
from typing import Optional

from domain import Car, ObstaclesDetector
from application import Application
from infrastructure import Motors, Leds, Buzzer, Ultrasonic, Servo
from .application_config import ApplicationConfig


class ApplicationBuilder:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, config: Optional[ApplicationConfig] = None) -> None:
        self.config = config or ApplicationConfig.development()
        self._app: Optional[Application] = None

    def build(self) -> Application:
        logging.basicConfig(level=self.config.log_level)
        self._logger.info(f"Building application with config: {self.config}")
        motors = Motors()
        leds = Leds()
        buzzer = Buzzer()
        car = Car(motors, leds, buzzer)
        obstacles_detector = ObstaclesDetector(Ultrasonic(), Servo())
        return Application(car, obstacles_detector)

    def __enter__(self):
        self._app = self.build()
        self._logger.info("Starting application...")
        self._app.start()
        return self._app

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._app is not None:
            try:
                self._logger.info("Stopping application...")
                self._app.stop()
            except Exception as e:
                self._logger.error(
                    f"Error during application shutdown: {e}", exc_info=True)
        return False
