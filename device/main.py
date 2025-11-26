import sys
import threading
import signal
import logging

from infrastructure import build_application

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    _logger = logging.getLogger(__name__)

    def signal_handler(sig, frame):
        _logger.info("Signal received, stopping...")
        stop_event.set()

    app = build_application()
    stop_event = threading.Event()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        _logger.info("Demo started")
        app.start()

        app.obstacles_detector_toggle_on_off()
        app.obstacles_detector_detect()
        app.obstacles_detector_toggle_on_off()
        app.car_toggle_on_off()
        app.car_move_forward()
        app.car_turn_right()
        app.car_stop()

        stop_event.wait()

    except KeyboardInterrupt:
        _logger.info("Closing...")
    except Exception as e:
        _logger.error(f"Error: {e}")
        app.stop()
        sys.exit(1)
    finally:
        _logger.info("Demo ended")
        app.stop()
