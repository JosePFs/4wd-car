import sys
import logging

from config_common import Command
from event import UpPressedEvent, DownPressedEvent, LeftPressedEvent, RightPressedEvent, SpacePressedEvent, ShiftPressedEvent
from application import ApplicationBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> int:
    try:
        with (ApplicationBuilder()
              .on(UpPressedEvent, Command.FORWARD)
              .on(DownPressedEvent, Command.BACKWARD)
              .on(LeftPressedEvent, Command.LEFT)
              .on(RightPressedEvent, Command.RIGHT)
              .on(SpacePressedEvent, Command.TOGGLE_CAR_ON_OFF)
              .on(ShiftPressedEvent, Command.TOGGLE_OBSTACLE_DETECTION_ON_OFF)) as _app:
            logger.info("Client started")

    except KeyboardInterrupt:
        logger.info("Client stopped")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
