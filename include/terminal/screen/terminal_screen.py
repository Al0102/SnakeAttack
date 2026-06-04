from abc import abstractmethod
from typing import List, Self, Tuple
from utils.types import ABCSingleton


class TerminalScreenBase(metaclass=ABCSingleton):
    @abstractmethod
    def __enter__(self) -> Self: ...

    @abstractmethod
    def __exit__(self) -> None: ...

    @staticmethod
    @abstractmethod
    def clear() -> None: ...

    @staticmethod
    @abstractmethod
    def get_size() -> Tuple[int, int]: ...

    @staticmethod
    @abstractmethod
    def set_size(columns: int, rows: int) -> None: ...

    @staticmethod
    @abstractmethod
    def check_is_inside(point: Tuple[int, int]
                        | List[int]) -> Tuple[int, int]: ...
