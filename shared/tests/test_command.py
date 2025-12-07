import pytest

from command import (
    ActivateMode,
    DeactivateMode,
    StopCarImmediately,
    ResumeCarMovement,
    DriveMode,
    MoveCarForward,
    MoveCarBackward,
    MoveCarLeft,
    MoveCarRight,
    parse_command,
)


def test_activate_manual_mode_encode(fixture_commands):
    command_name = "activate_mode:manual"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_activate_manual_mode_decode():
    cmd = parse_command("activate_mode:manual")
    assert isinstance(cmd, ActivateMode)
    assert cmd.mode == DriveMode.MANUAL


def test_activate_obstances_avoidance_mode_encode(fixture_commands):
    command_name = "activate_mode:obstances_avoidance"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_activate_obstances_avoidance_mode_decode():
    cmd = parse_command("activate_mode:obstances_avoidance")
    assert isinstance(cmd, ActivateMode)
    assert cmd.mode == DriveMode.OBSTANCES_AVOIDANCE


def test_activate_walls_following_mode_encode(fixture_commands):
    command_name = "activate_mode:walls_following"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_activate_walls_following_mode_decode():
    cmd = parse_command("activate_mode:walls_following")
    assert isinstance(cmd, ActivateMode)
    assert cmd.mode == DriveMode.WALLS_FOLLOWING


def test_deactivate_mode_encode(fixture_commands):
    command_name = "deactivate_mode"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_deactivate_mode_decode():
    cmd = parse_command("deactivate_mode")
    assert cmd == DeactivateMode()


def test_stop_car_immediately_encode(fixture_commands):
    command_name = "stop_car_immediately"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_stop_car_immediately_decode():
    cmd = parse_command("stop_car_immediately")
    assert cmd == StopCarImmediately()


def test_resume_car_movement_encode(fixture_commands):
    command_name = "resume_car_movement"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_resume_car_movement_decode():
    cmd = parse_command("resume_car_movement")
    assert cmd == ResumeCarMovement()


def test_move_car_forward_encode(fixture_commands):
    command_name = "move_car_forward"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_move_car_forward_decode():
    cmd = parse_command("move_car_forward")
    assert cmd == MoveCarForward()


def test_move_car_backward_encode(fixture_commands):
    command_name = "move_car_backward"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_move_car_backward_decode():
    cmd = parse_command("move_car_backward")
    assert cmd == MoveCarBackward()


def test_move_car_left_encode(fixture_commands):
    command_name = "move_car_left"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_move_car_left_decode():
    cmd = parse_command("move_car_left")
    assert cmd == MoveCarLeft()


def test_move_car_right_encode(fixture_commands):
    command_name = "move_car_right"
    cmd = fixture_commands[command_name]
    assert cmd.encode() == command_name.encode()


def test_move_car_right_decode():
    cmd = parse_command("move_car_right")
    assert cmd == MoveCarRight()


def test_invalid_drivemode_raises_valueerror():
    with pytest.raises(ValueError):
        DriveMode.from_string("invalid")


def test_invalid_command_decode_raises_valueerror():
    with pytest.raises(ValueError):
        parse_command("invalid")


@pytest.fixture
def fixture_commands():
    return {
        "activate_mode:manual": ActivateMode(mode=DriveMode.MANUAL),
        "activate_mode:obstances_avoidance": ActivateMode(
            mode=DriveMode.OBSTANCES_AVOIDANCE
        ),
        "activate_mode:walls_following": ActivateMode(mode=DriveMode.WALLS_FOLLOWING),
        "deactivate_mode": DeactivateMode(),
        "stop_car_immediately": StopCarImmediately(),
        "resume_car_movement": ResumeCarMovement(),
        "move_car_forward": MoveCarForward(),
        "move_car_backward": MoveCarBackward(),
        "move_car_left": MoveCarLeft(),
        "move_car_right": MoveCarRight(),
    }
