from pynput import keyboard
from typing import Union, Any
import termios
import sys
import tty

from event_handler import EventHandler
from event import (
    UpPressedEvent,
    DownPressedEvent,
    LeftPressedEvent,
    RightPressedEvent,
    SpacePressedEvent,
    ShiftPressedEvent,
    EscapePressedEvent,
)

W_KEY = keyboard.KeyCode.from_char("w")
S_KEY = keyboard.KeyCode.from_char("s")
A_KEY = keyboard.KeyCode.from_char("a")
D_KEY = keyboard.KeyCode.from_char("d")


class KeyboardController:
    def __init__(self, event_handler: EventHandler):
        self._event_handler = event_handler
        self._old_settings = None
        self._listener = None

    def on_press(self, key):
        try:
            if self._matches_key(key, keyboard.Key.up, W_KEY):
                self._event_handler.handle(UpPressedEvent())
            if self._matches_key(key, keyboard.Key.down, S_KEY):
                self._event_handler.handle(DownPressedEvent())
            if self._matches_key(key, keyboard.Key.left, A_KEY):
                self._event_handler.handle(LeftPressedEvent())
            if self._matches_key(key, keyboard.Key.right, D_KEY):
                self._event_handler.handle(RightPressedEvent())
            if self._matches_key(key, keyboard.Key.space):
                self._event_handler.handle(SpacePressedEvent())
            if self._matches_key(key, keyboard.Key.shift):
                self._event_handler.handle(ShiftPressedEvent())
            if key == keyboard.Key.esc:
                self._event_handler.handle(EscapePressedEvent())
        except Exception as e:
            print(f"Error: {e}")


    def _matches_key(self, key: Union[keyboard.Key, keyboard.KeyCode], *candidates: Any) -> bool:
        return any(key == candidate for candidate in candidates)

    def run(self):
        try:
            self._disable_echo()
            with keyboard.Listener(on_press=self.on_press) as self._listener:
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