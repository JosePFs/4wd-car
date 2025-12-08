import tempfile
import pytest
from pathlib import Path
import os

from env import Env


@pytest.fixture(autouse=True)
def clean_env():
    env_vars = ["APP_MODE", "UDP_PORT", "SERVER_HOST"]
    original = {k: os.environ.get(k) for k in env_vars}

    yield

    for k in env_vars:
        if original[k] is None:
            os.environ.pop(k, None)
        elif original[k] is not None:
            os.environ[k] = str(original[k])


@pytest.fixture
def create_env_file():
    created_files: list[Path] = []

    def _create(content: str) -> Path:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".env") as f:
            f.write(content)
            path = Path(f.name)
            created_files.append(path)
        return path

    yield _create

    for path in created_files:
        path.unlink(missing_ok=True)


def test_load_env(create_env_file):
    env_file = create_env_file("APP_MODE=test\nUDP_PORT=5678\nSERVER_HOST=127.0.0.1\n")
    env = Env(path=env_file)

    assert env.app_mode == "test"
    assert env.udp_port == 5678
    assert env.udp_host == "127.0.0.1"


def test_load_env_app_mode_not_found(create_env_file):
    env_file = create_env_file("UDP_PORT=5678\nSERVER_HOST=127.0.0.1\n")
    env = Env(path=env_file)

    with pytest.raises(ValueError):
        assert env.app_mode == "test"
        assert env.udp_port == 5678
        assert env.udp_host == "127.0.0.1"
