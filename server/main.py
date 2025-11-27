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
            command = udp_server.receive()
            match command:
                case Command.FORWARD:
                    logger.info("Forward")
                    app.car_move_forward()
                case Command.BACKWARD:
                    logger.info("Backward")
                    app.car_move_backward()
                case Command.LEFT:
                    logger.info("Left")
                    app.car_turn_left()
                case Command.RIGHT:
                    logger.info("Right")
                    app.car_turn_right()
                case Command.STOP:
                    logger.info("Stop")
                    app.car_stop()
                case Command.TOGGLE_CAR_ON_OFF:
                    logger.info("Toggle car on off")
                    app.car_toggle_on_off()
                case Command.TOGGLE_OBSTACLE_DETECTION_ON_OFF:
                    logger.info("Toggle obstacle detection on off")
                    app.obstacles_detector_toggle_on_off()
                case _:
                    logger.error(f"Unknown command: {command}")

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
