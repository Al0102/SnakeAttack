import sys

if sys.platform == "win32":
    from ._windows_screen import TerminalScreen
else:
    from ._posix_screen import TerminalScreen

__all__ = ["TerminalScreen"]
