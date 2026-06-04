from abc import abstractmethod
from typing import Self
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
    def __enter__(self) -> Self: ...

    @abstractmethod
    def __exit__(self) -> None: ...

    def get_key(self) -> str:
        self.buffer.append(self.poll())
        return self.buffer[-1]

    def peek_key(self) -> str:
        return "" if self.buffer == [] else self.buffer[-1]

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

