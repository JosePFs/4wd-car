from dotenv import load_dotenv
from pathlib import Path
import os
from typing import Protocol


class EnvironmentConfig(Protocol):
    @property
    def app_mode(self) -> str: ...
    @property
    def udp_port(self) -> int: ...
    @property
    def udp_host(self) -> str: ...


class Env(EnvironmentConfig):
    def __init__(self, path: Path | None = None):
        self._path = path or Path(__file__).parent / ".env"
        self._env: dict[str, str] = dict(os.environ)

        self._load()

    def _load(self):
        if not self._path.exists() or not self._path.is_file():
            raise FileNotFoundError(f"Environment file not found at {self._path}")

        load_dotenv(self._path, override=True)
        self._env.update(os.environ)

    @property
    def app_mode(self) -> str:
        value = self._env.get("APP_MODE")
        if value is None:
            raise ValueError(
                f"Environment variable APP_MODE is not set in {self._path}"
            )
        return value

    @property
    def udp_port(self) -> int:
        value = self._env.get("UDP_PORT")
        if value is None:
            raise ValueError(
                f"Environment variable UDP_PORT is not set in {self._path}"
            )
        return int(value)

    @property
    def udp_host(self) -> str:
        value = self._env.get("SERVER_HOST")
        if value is None:
            raise ValueError(
                f"Environment variable SERVER_HOST is not set in {self._path}"
            )
        return value
