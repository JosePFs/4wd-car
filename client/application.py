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
from shared import Command, EnvironmentConfig, Env


class Mode(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"

    def to_logging_level(self) -> int:
        return {
            Mode.DEVELOPMENT: logging.DEBUG,
            Mode.PRODUCTION: logging.INFO,
            Mode.TEST: logging.DEBUG,
        }[self]


@dataclass(frozen=True)
class ApplicationConfig:
    mode: Mode
    log_level: int
    udp_host: str
    udp_port: int

    @classmethod
    def development(cls) -> "ApplicationConfig":
        mode = Mode.DEVELOPMENT
        return cls(
            mode=mode,
            log_level=mode.to_logging_level(),
            udp_host="127.0.0.1",
            udp_port=5000,
        )

    @classmethod
    def production(cls) -> "ApplicationConfig":
        mode = Mode.PRODUCTION
        return cls(
            mode=mode,
            log_level=mode.to_logging_level(),
            udp_host="127.0.0.1",
            udp_port=5000,
        )

    @classmethod
    def test(cls) -> "ApplicationConfig":
        mode = Mode.TEST
        return cls(
            mode=mode,
            log_level=mode.to_logging_level(),
            udp_host="127.0.0.1",
            udp_port=5000,
        )

    @classmethod
    def from_env(cls, env: EnvironmentConfig = Env()) -> "ApplicationConfig":
        mode = Mode(env.app_mode)
        return cls(
            mode=mode,
            log_level=mode.to_logging_level(),
            udp_host=env.udp_host,
            udp_port=env.udp_port,
        )

    def __str__(self):
        return f"ApplicationConfig(mode={self.mode}, log_level={self.log_level})"


class Application:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, keyboard_controller: KeyboardController, udp_client: UDPClient):
        self._keyboard_controller = keyboard_controller
        self._udp_client = udp_client

    def run(self):
        self._logger.info("Running application...")
        self._keyboard_controller.run()

    def _stop(self):
        self._logger.info("Stopping application...")
        try:
            self._keyboard_controller.stop()
            self._udp_client.close()
        except Exception as e:
            self._logger.error(f"Error stopping application: {e}", exc_info=True)
            raise e

    @classmethod
    def builder(
        cls, config: Optional[ApplicationConfig] = None
    ) -> "ApplicationBuilder":
        return ApplicationBuilder(config)


class ApplicationBuilder:
    def __init__(self, config: Optional[ApplicationConfig] = None):
        self.config = config or ApplicationConfig.development()
        self._callbacks: list[
            tuple[type[Event], list[tuple[Optional[type[Event]], Command]]]
        ] = []
        self._last_event_type: Optional[type[Event]] = None
        self._app: Optional[Application] = None

    def on(self, event_type: type[Event], command: Command) -> "ApplicationBuilder":
        self._callbacks.append((event_type, [(None, command)]))
        self._last_event_type = event_type
        return self

    def then(self, event_type: type[Event], command: Command) -> "ApplicationBuilder":
        self._callbacks.append((event_type, [(self._last_event_type, command)]))
        return self

    def _build(self) -> Application:
        udp_client = UDPClient(UDPTarget(self.config.udp_host, self.config.udp_port))

        event_handler = EventHandler()
        for event_type, command_list in self._callbacks:
            for last_event_type, command in command_list:
                event_handler.add_callback(
                    last_event_type,
                    event_type,
                    partial(lambda event, cmd: udp_client.send(cmd), cmd=command),
                )
        keyboard_controller = KeyboardController(event_handler)

        return Application(keyboard_controller, udp_client)

    def __enter__(self):
        self._app = self._build()
        return self._app

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._app is not None:
            self._app._stop()
        return False
