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
from application import Application, ApplicationConfig


def main() -> int:
    app_config = ApplicationConfig.from_env()
    logging.basicConfig(level=app_config.log_level)

    try:
        with (
            Application.builder(app_config)
            .on(KeyOnePressedEvent, ActivateMode(DriveMode.MANUAL))
            .then(UpPressedEvent, MoveCarForward())
            .then(DownPressedEvent, MoveCarBackward())
            .then(LeftPressedEvent, MoveCarLeft())
            .then(RightPressedEvent, MoveCarRight())
            .then(KeyReleasedEvent, StopCarImmediately())
            .on(KeyTwoPressedEvent, ActivateMode(DriveMode.OBSTANCES_AVOIDANCE))
            .on(KeyThreePressedEvent, ActivateMode(DriveMode.WALLS_FOLLOWING))
            .on(KeyZeroPressedEvent, DeactivateMode())
            .on(SpacePressedEvent, StopCarImmediately())
            .on(ShiftLeftPressedEvent, ResumeCarMovement())
            .on(ShiftRightPressedEvent, ResumeCarMovement())
        ) as app:
            app.run()

    except KeyboardInterrupt:
        return 0
    except Exception as e:
        logging.getLogger(__name__).error(f"Error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
