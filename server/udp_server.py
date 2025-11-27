import socket
from dataclasses import dataclass
from typing import Optional
import logging
from logging import Logger

from config_common import Command


@dataclass(frozen=True)
class UDPPort:
    _port: int

    @property
    def port(self) -> int:
        return self._port


class UDPServer:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, port: UDPPort):
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.sock.bind(("", self._port.port))
        self._logger.info(f"UDP server started on port {self._port.port}")

    def receive(self) -> Optional[Command]:
        data, addr = self.sock.recvfrom(1024)
        self._logger.info(f"Message received from {addr}: {data}")
        try:
            command = Command.from_string(data.decode())
        except ValueError:
            self._logger.error(f"Invalid command: {data.decode()}")
            return None
        return command

    def __enter__(self):
        self._logger.info("Starting UDP server...")
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        return False
