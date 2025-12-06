import sys
import threading
import signal
from typing import Callable
from types import FrameType
import logging

from config_common import Command, Env
from udp_server import UDPServer, UDPPort
from device import ApplicationBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def signal_handler(stop_event: threading.Event) -> Callable[[int, FrameType | None], None]:
    def handler(_sig: int, _frame: FrameType | None) -> None:
        logger.info("Signal received, stopping...")
        stop_event.set()
    return handler


def main() -> int:
    stop_event = threading.Event()
    signal.signal(signal.SIGINT, signal_handler(stop_event))
    signal.signal(signal.SIGTERM, signal_handler(stop_event))

    try:
        env = Env().load()
        with (UDPServer(UDPPort(env.udp_port)) as udp_server, ApplicationBuilder() as app):
            udp_server.on(Command.FORWARD, app.car_move_forward)
            udp_server.on(Command.BACKWARD, app.car_move_backward)
            udp_server.on(Command.LEFT, app.car_turn_left)
            udp_server.on(Command.RIGHT, app.car_turn_right)
            udp_server.on(Command.STOP, app.car_stop)
            udp_server.on(Command.TOGGLE_CAR_ON_OFF, app.car_toggle_on_off)

            stop_event.wait()

    except KeyboardInterrupt:
        logger.info("Server stopped")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
