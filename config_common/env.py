from dotenv import load_dotenv
import os
from pathlib import Path

class Env:
    _path: Path = Path(__file__).parent / ".env"

    @staticmethod
    def load() -> "Env":
        load_dotenv(Env._path)
        return Env()

    @property
    def udp_port(self) -> int:
        value = os.getenv("UDP_PORT")
        if value is None:
            raise ValueError("Environment variable UDP_PORT is not set in {Env._path}")
        return int(value)

    @property
    def udp_host(self) -> str:
        value = os.getenv("SERVER_HOST")
        if value is None:
            raise ValueError("Environment variable SERVER_HOST is not set in {Env._path}")
        return value