from dotenv import load_dotenv
from pathlib import Path
import os


class Env:
    def __init__(self, path: Path | None = None, env: dict[str, str] | None = None):
        self._path = path or Path(__file__).parent / ".env"
        self._env: dict[str, str] = env if env is not None else dict(os.environ)

    def load(self) -> "Env":
        load_dotenv(self._path)
        self._env.update(os.environ)
        return self

    @property
    def udp_port(self) -> int:
        value = self._env.get("UDP_PORT")
        if value is None:
            raise ValueError(f"Environment variable UDP_PORT is not set in {self._path}")
        return int(value)

    @property
    def udp_host(self) -> str:
        value = self._env.get("SERVER_HOST")
        if value is None:
            raise ValueError(f"Environment variable SERVER_HOST is not set in {self._path}")
        return value
