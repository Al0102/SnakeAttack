from abc import abstractmethod
import select
import sys
from utils.types import ABCSingleton


class KeyInputBase(metaclass=ABCSingleton):
    def __init__(self):
        self.pressed = ""
        self.buffer = []

    @abstractmethod
    def poll(self) -> str: ...

    @abstractmethod
    def has_waiting(self) -> int | bool: ...

    @abstractmethod
    def __enter__(self) -> any: ...

    @abstractmethod
    def __exit__(self) -> None: ...

    def get_key(self) -> str:
        self.buffer.append(self.poll())
        return self.buffer[-1]

    def pull_key(self) -> str:
        return "" if self.buffer == [] else self.buffer.pop(0)

    def pull_keys(self, amount=1) -> str | list:
        if amount <= 1:
            return [self.buffer.pop(0)] if self.buffer else []
        elif amount >= len(self.buffer):
            return self.flush_keys()
        else:
            _pop = self.buffer[len(self.buffer) - amount:]
            return _pop

    def flush_keys(self) -> list:
        _buffer = self.buffer
        self.buffer.clear()
        return _buffer

"""
class _PosixKeyInput(_KeyInput):
    def __init__(self):
        # Control codes for POSIX/WINDOWS
        # UP DOWN RIGHT LEFT
        if is_posix():
            tty.setraw(fd)
            CONTROL_CODES = tuple(range(65,69), 3)
        else:
            CONTROL_CODES = (72, 80, 77, 75, b'\x03')
        self.CONTROL_MAP = dict(
            CONTROL_CODES, (
                "up", "down", "left", "right"
            )
        )

    def _scan_in_control_codes(self, char):
        if char in self.CONTROL_MAP:
            return self.CONTROL_MAP[char]
        self.key_mash_counter += 1
        return KEY.QUIT if self.key_mash_counter > self.max_control_code_mash else 0
        # Uncomment if you want to raise error for control codes that are not coded in yet
        # raise ValueError(f'Invalid control code: {char}')
        
    def keyIn(self):
        if POSIX:
            # Reads one chracter from input stream 
            char = ord(sys.stdin.read(1))
        else:
            # Gets keyboard input as UNICODE character
            # ord() converts to ascii
            key = msvcrt.getwch()
            char = ord(key)

        # ASCII (a - ~)
        if 32 <= char <= 126:
            self.pressed = char
            self.key_mash_counter = 0

        # Backspace
        elif char == 8:
# Test -             render("\033[3;5H Backspace")
            self.pressed = KEY.BACKSPACE
            self.key_mash_counter = 0
        # Tab
        elif char == 9:
# Test -             render("\033[3;5H TAB")
            self.pressed = KEY.TAB
            self.key_mash_counter = 0
        # ENTER
        elif char in {10, 13}:
# Test -             render("\033[3;5H ENTER")
            self.pressed = KEY.ENTER
            self.key_mash_counter = 0
        # CTRL-C
        if char == 3:
            self.pressed = KEY.QUIT
            self.key_mash_counter = 0

        if POSIX:
            if char == 27:
                # Control codes
                next1 = ord(sys.stdin.read(1))
                if next1 == 91:
                    next2 = ord(sys.stdin.read(1))
# Test -                     render("\033[1;5H CONTROL")
                    self.pressed = self._scan_in_control_codes(next2)
                    if self.pressed != 0: self.key_mash_counter = 0
# Test -                     match self.pressed:
# Test -                         case CONTROLS.UP: 
# Test -                             render("^")
# Test -                         case CONTROLS.DOWN: 
# Test -                             render("v")
# Test -                         case CONTROLS.RIGHT: 
# Test -                             render(">")
# Test -                         case CONTROLS.LEFT: 
# Test -                             render("<")
# Test -                         case _:
# Test -                             render(str(char))
                else:
                    # ESCAPE - If no control codes are inputted,
                    #          ESC is being pressed
                    self.pressed = CONTROLS.ESCAPE
            return self.pressed

        # WINDOWS
        else:
            # Control codes
            if char == 0x00 or char == 0xE0:
                next_ = ord(msvcrt.getwch())
# Test -                 render("\033[2;5H CONTROL")
                self.pressed = self._scan_in_control_codes(next_)
                if self.pressed != 0: self.key_mash_counter = 0
# Test -                 match self.pressed:
# Test -                     case CONTROLS.UP: 
# Test -                         render("^")
# Test -                     case CONTROLS.DOWN: 
# Test -                         render("v")
# Test -                     case CONTROLS.RIGHT: 
# Test -                         render(">")
# Test -                     case CONTROLS.LEFT: 
# Test -                         render("<")
# Test -                     case _:
# Test -                         render(str(char))

            elif char == 27: #ESC
# Test -                 render("\033[3;5H ESCAPE")
                self.pressed = CONTROLS.ESCAPE
            return self.pressed

        self.pressed = KEY.QUIT

"""