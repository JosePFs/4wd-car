from pynput import keyboard
from enum import Enum
from typing import Union, Any, Optional
import termios
import sys
import tty
import logging
from logging import Logger

from event_handler import EventHandler
from event import (
    UpPressedEvent,
    DownPressedEvent,
    LeftPressedEvent,
    RightPressedEvent,
    KeyZeroPressedEvent,
    KeyOnePressedEvent,
    KeyTwoPressedEvent,
    KeyThreePressedEvent,
    KeyReleasedEvent,
    ShiftLeftPressedEvent,
    ShiftRightPressedEvent,
    SpacePressedEvent,
)


ZERO_KEY = keyboard.KeyCode.from_char("0")
ONE_KEY = keyboard.KeyCode.from_char("1")
TWO_KEY = keyboard.KeyCode.from_char("2")
THREE_KEY = keyboard.KeyCode.from_char("3")
W_KEY = keyboard.KeyCode.from_char("w")
S_KEY = keyboard.KeyCode.from_char("s")
A_KEY = keyboard.KeyCode.from_char("a")
D_KEY = keyboard.KeyCode.from_char("d")


class KeyEventMap(Enum):
    ZERO = (ZERO_KEY, KeyZeroPressedEvent)
    ONE = (ONE_KEY, KeyOnePressedEvent)
    TWO = (TWO_KEY, KeyTwoPressedEvent)
    THREE = (THREE_KEY, KeyThreePressedEvent)
    UP = (keyboard.Key.up, UpPressedEvent)
    W = (W_KEY, UpPressedEvent)
    DOWN = (keyboard.Key.down, DownPressedEvent)
    S = (S_KEY, DownPressedEvent)
    LEFT = (keyboard.Key.left, LeftPressedEvent)
    A = (A_KEY, LeftPressedEvent)
    RIGHT = (keyboard.Key.right, RightPressedEvent)
    D = (D_KEY, RightPressedEvent)
    SHIFT_LEFT = (keyboard.Key.shift_l, ShiftLeftPressedEvent)
    SHIFT_RIGHT = (keyboard.Key.shift_r, ShiftRightPressedEvent)
    SPACE = (keyboard.Key.space, SpacePressedEvent)

    @classmethod
    def listen_to_release(cls, key: keyboard.Key | keyboard.KeyCode) -> bool:
        return any(
            candidate
            for candidate in cls.__iter__()
            if key == candidate.value[0] and candidate.value[1].should_send_release()
        )

    @classmethod
    def get_on_press(
        cls, key: keyboard.Key | keyboard.KeyCode
    ) -> Optional["KeyEventMap"]:
        return next(
            (candidate for candidate in cls.__iter__() if key == candidate.value[0]),
            None,
        )


class KeyboardController:
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, event_handler: EventHandler):
        self._event_handler = event_handler
        self._old_settings = None
        self._listener = None

    def on_release(self, key):
        try:
            if KeyEventMap.listen_to_release(key):
                self._event_handler.handle(KeyReleasedEvent(key))
        except Exception as e:
            self._logger.error(f"Error on release: {e}", exc_info=True)

    def on_press(self, key):
        try:
            event_class = KeyEventMap.get_on_press(key)
            if event_class is not None:
                self._event_handler.handle(event_class.value[1](key))
            elif key == keyboard.Key.esc:
                self.stop()
        except Exception as e:
            self._logger.error(f"Error on press: {e}", exc_info=True)

    def _matches_key(
        self, key: Union[keyboard.Key, keyboard.KeyCode], *candidates: Any
    ) -> bool:
        return any(key == candidate for candidate in candidates)

    def run(self):
        try:
            self._disable_echo()
            with keyboard.Listener(
                on_press=self.on_press, on_release=self.on_release
            ) as self._listener:
                self._listener.join()
        finally:
            self.stop()

    def stop(self):
        if self._listener:
            self._listener.stop()
        self._restore_echo()

    def _disable_echo(self):
        if sys.stdin.isatty():
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def _restore_echo(self):
        if self._old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)
