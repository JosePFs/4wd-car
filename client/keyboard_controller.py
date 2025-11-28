from pynput import keyboard
from typing import Union, Any
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
    ShiftLeftPressedEvent,
    ShiftRightPressedEvent,
    KeyReleasedEvent,
)

W_KEY = keyboard.KeyCode.from_char("w")
S_KEY = keyboard.KeyCode.from_char("s")
A_KEY = keyboard.KeyCode.from_char("a")
D_KEY = keyboard.KeyCode.from_char("d")

class KeyboardController:
    _logger: Logger = logging.getLogger(__name__)
    _key_event_map = {
        keyboard.Key.up: UpPressedEvent,
        W_KEY: UpPressedEvent,
        keyboard.Key.down: DownPressedEvent,
        S_KEY: DownPressedEvent,
        keyboard.Key.left: LeftPressedEvent,
        A_KEY: LeftPressedEvent,
        keyboard.Key.right: RightPressedEvent,
        D_KEY: RightPressedEvent,
        keyboard.Key.shift_l: ShiftLeftPressedEvent,
        keyboard.Key.shift_r: ShiftRightPressedEvent,
    }

    def __init__(self, event_handler: EventHandler):
        self._event_handler = event_handler
        self._old_settings = None
        self._listener = None

    def on_release(self, key):
        try:
            if key not in self._key_event_map:
                return
            self._event_handler.handle(KeyReleasedEvent(key))
        except Exception as e:
            self._logger.error(f"Error on release: {e}", exc_info=True)

    def on_press(self, key):
        try:
            if key in self._key_event_map:
                event_class = self._key_event_map[key]
                self._event_handler.handle(event_class())
            elif key == keyboard.Key.esc:
                self.stop()
        except Exception as e:
            self._logger.error(f"Error on press: {e}", exc_info=True)

    def _matches_key(self, key: Union[keyboard.Key, keyboard.KeyCode], *candidates: Any) -> bool:
        return any(key == candidate for candidate in candidates)

    def run(self):
        try:
            self._disable_echo()
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self._listener:
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
