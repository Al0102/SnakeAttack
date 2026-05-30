from msvcrt import getwch, kbhit
import sys

from terminal.input.key_input import KeyInputBase


class KeyInput(KeyInputBase):
    CONTROL_KEY_MAP = {
        # Require 1 extra getch() call after yielding \xe0
        "extend": "\xe0",
        # H: \x48, K: \x4B, M: \x4D, P: \x50
        "\x1b": "escape",
        "\x1bH": "up",
        "\x1bK": "left",
        "\x1bM": "right",
        "\x1bP": "down",

        "\x08": "backspace",
        "\t": "tab",
        "\r": "enter",
        "\n": "enter",
    }

    def __init__(self):
        super().__init__()

        self.key_mash_counter = 0
        self.max_control_code_mash = 5

    def __enter__(self) -> any:
        """
        Saves the old terminal settings and sets non-blocking key inputs.

        :return KeyInputBase: the object for the context manager
        """
        return self

    def __exit__(self, _, __, traceback) -> None:
        """
        Prints errors with manager.
        """
        if traceback:
            print(traceback, file=sys.stderr)

    def poll(self, raw=False) -> str:
        if not self.has_waiting():
            return None
        code = getwch()
        if code == KeyInput.CONTROL_KEY_MAP["extend"]:
            code = "\x1b" + getwch()
        # Normal characters and undefined actions
        if not (raw or code.isprintable()):
            return KeyInput.CONTROL_KEY_MAP.get(code, "unknown")
        return code

    def has_waiting(self, _=0) -> int | bool:
        return kbhit()
