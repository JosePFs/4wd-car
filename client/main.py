import sys
import logging

from shared.command import (
    ActivateMode,
    DeactivateMode,
    DriveMode,
    StopCarImmediately,
    ResumeCarMovement,
    MoveCarForward,
    MoveCarBackward,
    MoveCarLeft,
    MoveCarRight,
)
from event import (
    KeyOnePressedEvent,
    KeyTwoPressedEvent,
    KeyThreePressedEvent,
    KeyZeroPressedEvent,
    ShiftLeftPressedEvent,
    ShiftRightPressedEvent,
    SpacePressedEvent,
    UpPressedEvent,
    DownPressedEvent,
    LeftPressedEvent,
    RightPressedEvent,
    KeyReleasedEvent,
)
from application import ApplicationBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> int:
    try:
        with (
            ApplicationBuilder()
            .on(UpPressedEvent, MoveCarForward())
            .on(DownPressedEvent, MoveCarBackward())
            .on(LeftPressedEvent, MoveCarLeft())
            .on(RightPressedEvent, MoveCarRight())
            .on(KeyReleasedEvent, StopCarImmediately())
            .on(KeyOnePressedEvent, ActivateMode(DriveMode.MANUAL))
            .on(KeyTwoPressedEvent, ActivateMode(DriveMode.OBSTANCES_AVOIDANCE))
            .on(KeyThreePressedEvent, ActivateMode(DriveMode.WALLS_FOLLOWING))
            .on(KeyZeroPressedEvent, DeactivateMode())
            .on(SpacePressedEvent, StopCarImmediately())
            .on(ShiftLeftPressedEvent, ResumeCarMovement())
            .on(ShiftRightPressedEvent, ResumeCarMovement())
        ) as _app:
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
