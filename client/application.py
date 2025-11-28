from enum import Enum
from dataclasses import dataclass
from typing import Optional
from functools import partial
import logging
from logging import Logger

from keyboard_controller import KeyboardController
from udp_client import UDPClient, UDPTarget
from event_handler import EventHandler
from event import Event
from config_common import Env, Command


class Mode(Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TEST = 'test'


@dataclass(frozen=True)
class ApplicationConfig:
    mode: Mode
    log_level: int

    @classmethod
    def development(cls) -> 'ApplicationConfig':
        return cls(mode=Mode.DEVELOPMENT, log_level=logging.DEBUG)

    @classmethod
    def production(cls) -> 'ApplicationConfig':
        return cls(mode=Mode.PRODUCTION, log_level=logging.INFO)

    @classmethod
    def test(cls) -> 'ApplicationConfig':
        return cls(mode=Mode.TEST, log_level=logging.DEBUG)

    def __str__(self):
        return f"ApplicationConfig(mode={self.mode}, log_level={self.log_level})"


class Application:
    def __init__(self, keyboard_controller: KeyboardController, udp_client: UDPClient):
        self._keyboard_controller = keyboard_controller
        self._udp_client = udp_client

    def run(self):
        self._keyboard_controller.run()

    def stop(self):
        self._keyboard_controller.stop()
        self._udp_client.close()


class ApplicationBuilder:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, config: Optional[ApplicationConfig] = None):
        self.config = config or ApplicationConfig.development()
        self._callbacks: list[tuple[type[Event], Command]] = []
        self._app: Optional[Application] = None

    def on(self, event_type: type[Event], command: Command) -> 'ApplicationBuilder':
        self._callbacks.append((event_type, command))
        return self

    def build(self) -> Application:
        logging.basicConfig(level=self.config.log_level)
        self._logger.info(f"Building application with config: {self.config}")
        env = Env().load()
        udp_client = UDPClient(UDPTarget(env.udp_host, env.udp_port))
        event_handler = EventHandler()
        for event_type, command in self._callbacks:
            event_handler.add_callback(
                event_type, partial(lambda event, cmd: udp_client.send(cmd), cmd=command))
        keyboard_controller = KeyboardController(event_handler)
        return Application(keyboard_controller, udp_client)

    def __enter__(self):
        self._app = self.build()
        self._logger.info("Starting application...")
        self._app.run()
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
