from dataclasses import dataclass
from enum import Flag, auto
from typing import List, Tuple


class ColourFormat(Flag):
    NAME = auto()
    RGB = auto()
    HEX = auto()


@dataclass
class Colour(frozen=True):
    # Lowercase
    name: str = None
    # 24-bit (red: 0-255, green: 0-255, blue: 0-255)
    rgb: Tuple[int, int, int] | List[int] = None
    # Integer representation of hex code (e.g. 0xaffe08 or 11533832)
    hexcode: int = None

    def get_formats(self) -> ColourFormat:
        _formats = 0
        if self.name is not None:
            _formats |= ColourFormat.NAME
        if self.rgb is not None:
            _formats |= ColourFormat.RGB
        if self.hexcode is not None:
            _formats |= ColourFormat.HEX
        return _formats
