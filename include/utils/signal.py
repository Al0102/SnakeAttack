

import sys
from typing import Callable, Dict, Tuple

from utils.utilities import match_type


class Signal:
    def __init__(self, *args: Tuple[type, ...], **kwargs: Dict[str, type]):
        self._connections = set()
        self._argument_types = args
        self._keyword_argument_types = kwargs
        print(args, kwargs)

    def connect(self, receiver: Callable) -> None:
        self._connections.add(receiver)

    def disconnect(self, callable: Callable) -> None:
        self._connections.remove(callable)

    # TODO: this should really be calling async functions
    def emit(self, *args, **kwargs):
        if not self._is_valid_emit(*args, **kwargs):
            raise TypeError(
                "Signal requires arguments of types:\n"
                f"[{self._argument_types}, {self._keyword_argument_types}].\n"
                f"Received [{tuple(map(lambda arg: type(arg), args))}, {kwargs}]")
        for receiver in self._connections:
            receiver(*args, **kwargs)

    def _is_valid_emit(self, *args, **kwargs) -> bool:
        # Arguments
        _valid_args_len = len(args) == len(self._argument_types)
        if not _valid_args_len:
            print("Invalid emit, not enough arguments", sys.stderr)
            return False
        _valid_args_types = any(
            map(match_type, args, self._argument_types))
        if not _valid_args_types:
            print("Invalid emit, incorrect argument types", sys.stderr)
            return False
        # Keyword arguments
        if len(self._keyword_argument_types) == 0:
            return True
        _valid_kwargs_keys = kwargs.keys() == self._keyword_argument_types.keys()
        if not _valid_kwargs_keys:
            print("Invalid emit, incorrect keyword argument list", sys.stderr)
            return False
        _valid_kwargs_values_types = any(map(
            lambda keyword: match_type(
                kwargs[keyword],
                self._keyword_argument_types[keyword]),
            kwargs.keys()))
        if not _valid_kwargs_values_types:
            print("Invalid emit, incorrect keyword argument types", sys.stderr)
            return False
