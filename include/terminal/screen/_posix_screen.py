"""
    POSIX terminal screen handling and modification.
"""
import os
import sys
from typing import Self

from terminal.screen.terminal_screen import TerminalScreenBase


class TerminalScreen(TerminalScreenBase):
    STD_OUTPUT_HANDLE = -11

    def __enter__(self) -> Self:
        return self

    def __exit__(self, _, __, traceback) -> None:
        if traceback:
            print(traceback, file=sys.stderr)

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
        return tuple(map(lambda coordinate: 0 < coordinate[0] <= coordinate[1], zip(point, TerminalScreen.get_size())))
