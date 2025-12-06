import tempfile
import pytest
from dotenv import load_dotenv
from pathlib import Path

from env import Env


def test_load_env_from_dict():    
    fake_env = {"UDP_PORT": "5678", "SERVER_HOST": "127.0.0.1"}
    env = Env(env=fake_env)
    assert env.udp_port == 5678
    assert env.udp_host == "127.0.0.1"


def test_load_env_from_file():
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp_file:
        tmp_file.write("UDP_PORT=5678\nSERVER_HOST=127.0.0.1\n")
        temp_path = tmp_file.name

    load_dotenv(temp_path)
    env = Env(path=Path(temp_path))
    assert env.udp_port == 5678
    assert env.udp_host == "127.0.0.1"


def test_load_env_udp_port_not_found():
    with pytest.raises(ValueError):
        Env(env={"SERVER_HOST": "127.0.0.1"}).udp_port


def test_load_env_udp_host_not_found():
    with pytest.raises(ValueError):
        Env(env={"UDP_PORT": "5678"}).udp_host