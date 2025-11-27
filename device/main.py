import sys
import threading
import signal
from typing import Callable
from types import FrameType
import logging

from infrastructure import ApplicationBuilder

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
        with ApplicationBuilder() as app:
            logger.info("Demo started")
            app.obstacles_detector_toggle_on_off()
            app.obstacles_detector_detect()
            app.obstacles_detector_toggle_on_off()
            app.car_toggle_on_off()
            app.car_move_forward()
            app.car_turn_right()
            app.car_stop()

            stop_event.wait()

    except KeyboardInterrupt:
        logger.info("Device stopped")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1
    finally:
        logger.info("Demo ended")

    return 0


if __name__ == "__main__":
    sys.exit(main())
