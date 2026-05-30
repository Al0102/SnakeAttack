import sys

if sys.platform == "win32":
    from ._windows import KeyInput
else:
    from ._posix import KeyInput

__all__ = ["KeyInput"]