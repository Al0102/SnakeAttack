import sys

if sys.platform == "win32":
    from ._windows_key_input import KeyInput
else:
    from ._posix_key_input import KeyInput

__all__ = ["KeyInput"]