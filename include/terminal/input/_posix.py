"""
    POSIX key input via termios
"""
import select
import sys
import termios

from terminal.input.key_input import KeyInputBase


class KeyInput(KeyInputBase):
    CONTROL_KEY_MAP = {
        "\x1b": "escape",
        "\x1b[A": "up",
        "\x1b[B" : "down",
        "\x1b[C": "right",
        "\x1b[D": "left",

        "\x7f": "backspace",
        "\t": "tab",
        "\n": "enter",

        "\x1bOP": "f1",
        "\x1bOQ": "f2",
        "\x1bOR": "f3",
        "\x1bOS": "f4",
    }

    def __init__(self):
        super().__init__()

        self.key_mash_counter = 0
        self.max_control_code_mash = 5

    # Source - https://stackoverflow.com/a/31736883
    # Posted by Phylliida, modified by community.
    # Retrieved 2026-05-28, License - CC BY-SA 4.0
    def __enter__(self) -> any:
        """
        Saves the old terminal settings and sets non-blocking key inputs.

        :return KeyInputBase: the object for the context manager
        """
        # Save the terminal settings
        self.file_descriptor = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.file_descriptor)
        self.old_term = termios.tcgetattr(self.file_descriptor)

        # New terminal setting unbuffered
        _LOCAL_FLAGS = 3
        self.new_term[_LOCAL_FLAGS] = (
            self.new_term[_LOCAL_FLAGS]
            # Non-canonical - Input available immediately
            & ~termios.ICANON
            # No echo - does not "echo" or print input
            & ~termios.ECHO)
        termios.tcsetattr(
            self.file_descriptor,
            # Settings apply after writes and existing input is discarded
            termios.TCSAFLUSH,
            self.new_term
        )
        return self

    def __exit__(self, _, __, traceback) -> None:
        """
        Resets the terminal to the original settings.
        """
        if traceback:
            print(traceback, file=sys.stderr)
        termios.tcsetattr(
            self.file_descriptor,
            termios.TCSAFLUSH,
            self.old_term
        )

    def poll(self, raw=False) -> str:
        _buffered = self.has_waiting()
        if not _buffered:
            return ""
        _data = sys.stdin.read(_buffered)
        if not (raw or _data.isprintable()):
            return KeyInput.CONTROL_KEY_MAP.get(_data, "unknown")
        return _data

    def has_waiting(self, timeout=0) -> int | bool:
        data_read, _, __ = select.select([sys.stdin], [], [], timeout)
        if data_read == []:
            return 0
        return len(data_read[0].buffer.peek())
