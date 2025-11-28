import socket
from threading import Thread, Event
from dataclasses import dataclass
from typing import Optional, Callable
import logging
from logging import Logger

from config_common import Command


@dataclass(frozen=True)
class UDPPort:
    _port: int

    @property
    def port(self) -> int:
        return self._port


class UDPServer(Thread):
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, port: UDPPort):
        super().__init__(daemon=False)
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._callbacks: dict[Command, Callable[[], None]] = {}

        self._stop_event = Event()

    def run(self) -> None:
        self._start()
        while not self._stop_event.is_set():
            try:
                command = self._receive()
                if command is not None:
                    self._handle_command(command)
            except Exception as e:
                self._logger.error(f"Error receiving command: {e}")
                continue

    def on(self, command: Command, callback: Callable[[], None]) -> None:
        self._callbacks[command] = callback

    def _receive(self) -> Optional[Command]:
        data, addr = self.sock.recvfrom(1024)
        self._logger.info(f"Message received from {addr}: {data}")
        try:
            command = Command.from_string(data.decode())
        except ValueError:
            self._logger.error(f"Invalid command: {data.decode()}")
            return None
        return command

    def _handle_command(self, command: Command) -> None:
        if command in self._callbacks:
            self._callbacks[command]()
        else:
            self._logger.error(f"No callback registered for command: {command}")

    def _start(self):
        self.sock.bind(("", self._port.port))
        self._logger.info(f"UDP server started on port {self._port.port}")
        self.start()

    def __enter__(self):
        self._logger.info("Starting UDP server...")
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        self.sock.close()
        self.join()
        return False
