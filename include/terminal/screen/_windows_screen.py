"""
    Windows terminal screen handling and modification.
"""
import os
import sys
import ctypes
from typing import Self

from terminal.screen.terminal_screen import TerminalScreenBase


class TerminalScreen(TerminalScreenBase):
    STD_OUTPUT_HANDLE = -11

    def __enter__(self) -> Self:
        """
        Saves the old terminal settings and enables virtual process handling for conhost.

        :return TerminalScreenBase: the object for the context manager
        """
        # Process control codes (e.g. \n) instead of displaying raw text
        ENABLE_PROCESSED_OUTPUT = 0x0001
        # (Disable) Wrap text overflow
        ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
        # Process escape sequences (e.g. \x1b[, \003[) instead of displaying raw text
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

        _handle = ctypes.windll.kernel32.GetStdHandle(TerminalScreen.STD_OUTPUT_HANDLE)

        # Save old settings
        self._old_settings = ctypes.c_ulong()
        ctypes.windll.kernel32.GetConsoleMode(
            _handle, ctypes.byref(self._old_settings))
        # Set new settings
        _new_settings = self._old_settings.value | (
            ENABLE_PROCESSED_OUTPUT &
            ~ENABLE_WRAP_AT_EOL_OUTPUT |
            ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        ctypes.windll.kernel32.SetConsoleMode(_handle, _new_settings)
        return self

    def __exit__(self, _, __, traceback) -> None:
        """
        Prints errors with manager.
        """
        if traceback:
            print(traceback, file=sys.stderr)
        _handle = ctypes.windll.kernel32.GetStdHandle(TerminalScreen.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleMode(
            _handle, self._old_settings.value)

    @staticmethod
    def clear():
        """
        Clear the terminal screen based on the operating system.

        :precondition: terminal must be run from a Windows or Posix style system
        :postcondition: clear the terminal screen based on the operating system
        """
        print("\033[2J\033[1H", end="", flush=True)

    @staticmethod
    def get_size():
        """
        Get the dimensions of the terminal as a tuple.

        :postcondition: get a tuple representing the width and height of the terminal
        :return: a tuple of two integers representing the width and height of the terminal
        """
        try:
            dimensions = os.get_terminal_size()
        except OSError:
            print("TerminalScreen.get_size: Invalid terminal, cannot get size.")
            return None
        else:
            return (dimensions.columns, dimensions.lines)

    @staticmethod
    def set_size(columns: int, rows: int):
        """
        Set the dimensions of the terminal as a tuple.

        :param columns (int): the new columns or width of the screen
        :param row (int): the new rows or height of the screen
        :postcondition: set the terminal screen size
        """
        print(f"\033[8;{rows};{columns}t", end="", flush=True)

    @staticmethod
    def check_is_inside(point: tuple | list) -> tuple:
        """
        Return <point> mapped to whether the value is within the terminal.

        Returned tuple has form: (<column_within boolean>, <row_within boolean>)

        :param point: a tuple of 2 integers representing the position to check
        :precondition: point must be a tuple of 2 integers
        :postcondition: get whether each value of <point> is within the terminal screen
        :postcondition: returned tuple has form: (<column_within boolean>, <row_within boolean>)
        :return: a tuple of 2 booleans representing whether each value in <point> is within the terminal screen
        """
        return tuple(map(lambda coordinate: 0 < coordinate[0] <= coordinate[1], zip(point, TerminalScreen.TerminalScreen.get_size())))
