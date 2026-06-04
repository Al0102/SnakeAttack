"""
    Terminal information and manipulation.
"""
import os
import subprocess
import sys


def clear_screen():
    """
    Clear the terminal screen based on the operating system.

    :precondition: terminal must be run from a Windows or Posix style system
    :postcondition: clear the terminal screen based on the operating system
    """
    subprocess.run("cls" if sys.platform == "win32" else "clear")


def get_screen_size():
    """
    Get the dimensions of the terminal as a tuple.

    :postcondition: get a tuple representing the width and height of the terminal
    :return: a tuple of two integers representing the width and height of the terminal
    """
    try:
        dimensions = os.get_terminal_size()
    except OSError:
        print("get_screen_size: Invalid terminal, cannot get size.")
        return None
    else:
        return (dimensions.columns, dimensions.lines)


def set_screen_size(columns: int, rows: int):
    """
    Set the dimensions of the terminal as a tuple.

    :param columns (int): the new columns or width of the screen
    :param row (int): the new rows or height of the screen
    :postcondition: set the terminal screen size
    """
    if sys.platform == "win32":
        os.system(f"mode con: cols={columns} lines={rows}")
    else:
        print(f"\033[8;{rows};{columns}t", end="", flush=True)


def point_within_screen(point: tuple | list) -> tuple:
    """
    Return <point> mapped to whether the value is within the terminal.

    Returned tuple has form: (<column_within boolean>, <row_within boolean>)

    :param point: a tuple of 2 integers representing the position to check
    :precondition: point must be a tuple of 2 integers
    :postcondition: get whether each value of <point> is within the terminal screen
    :postcondition: returned tuple has form: (<column_within boolean>, <row_within boolean>)
    :return: a tuple of 2 booleans representing whether each value in <point> is within the terminal screen
    """
    return tuple(map(lambda coordinate: 0 < coordinate[0] <= coordinate[1], zip(point, get_screen_size())))


def main():
    """
    Drive the program.
    """
    print("Terminal columns (width) and rows (height)")
    print(get_screen_size())
    print("Clear screen after input...")
    input()
    clear_screen()


if __name__ == '__main__':
    main()
