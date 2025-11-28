import socket
from dataclasses import dataclass
import logging
from logging import Logger

from config_common import CommandWithKey

@dataclass(frozen=True)
class UDPTarget:
    host: str
    port: int

    @property
    def address(self) -> tuple[str, int]:
        return self.host, self.port

class UDPClient:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, target: UDPTarget):
        self.target = target
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg: CommandWithKey):
        self.sock.sendto(str(msg).encode(), self.target.address)
        self._logger.info(f"Message sent: {msg} to {self.target.address}")

    def close(self):
        self.sock.close()