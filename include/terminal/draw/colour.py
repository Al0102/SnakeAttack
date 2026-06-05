from dataclasses import dataclass
from enum import IntFlag, auto
from typing import List, Tuple

from ansi_actions.style import Style, get_styles


class ColourFormat(IntFlag):
    NAME = auto()
    RGB = auto()
    HEX = auto()


@dataclass(frozen=True)
class Colour():
    # Lowercase
    name: str = None
    # 24-bit (red: 0-255, green: 0-255, blue: 0-255)
    rgb: Tuple[int, int, int] | List[int] = None
    # Integer representation of hex code (e.g. 0xaffe08 or 11533832)
    hexint: int = None

    def get_formats(self) -> ColourFormat:
        _formats = 0
        if self.name is not None:
            _formats |= ColourFormat.NAME
        if self.rgb is not None:
            _formats |= ColourFormat.RGB
        if self.hexint is not None:
            _formats |= ColourFormat.HEX
        return _formats

    def front(self) -> str:
        if self.get_formats() & ColourFormat.NAME:
            _colour = self.name.upper()
            if _colour in Style.__members__:
                return get_styles().get(Style[_colour], "")
        if self.get_formats() & ColourFormat.RGB:
            return Colour.rgb_to_ansii_front(self.rgb)
        if self.get_formats() & ColourFormat.HEX:
            return Colour.rgb_to_ansii_front(Colour.hexint_to_rgb(self.hexint))
        return ""

    def back(self) -> str:
        if self.get_formats() & ColourFormat.NAME:
            _colour = "BACKGROUND_" + self.name.upper()
            if _colour in Style.__members__:
                return get_styles().get(Style[_colour], "")
        if self.get_formats() & ColourFormat.RGB:
            return Colour.rgb_to_ansii_back(self.rgb)
        if self.get_formats() & ColourFormat.HEX:
            return Colour.rgb_to_ansii_back(Colour.hexint_to_rgb(self.hexint))
        return ""

    @staticmethod
    def hexint_to_rgb(value: int) -> Tuple[int, int, int]:
        red = (value >> 16) & 255
        green = (value >> 8) & 255
        blue = value & 255
        return (red, green, blue)

    @staticmethod
    def rgb_to_ansii_front(rgb: Tuple[int, int, int] | List[int]) -> str:
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    @staticmethod
    def rgb_to_ansii_back(rgb: Tuple[int, int, int] | List[int]) -> str:
        return f"\033[42;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


class Colours:
    NONE = Colour()
    BLACK = Colour(name="black", rgb=(0, 0, 0), hexint=0x000000)
    WHITE = Colour(name="white", rgb=(255, 255, 255), hexint=0xffffff)
    RED = Colour(name="red", rgb=(255, 0, 0), hexint=0xff0000)
    YELLOW = Colour(name="yellow", rgb=(250, 202, 1), hexint=0xfaca01)
    MAGENTA = Colour(name="magenta", rgb=(204, 34, 228), hexint=0xcc22e4)
    CYAN = Colour(name="cyan", rgb=(66, 160, 255), hexint=0x42a0ff)
    GREEN = Colour(name="green", rgb=(0, 255, 0), hexint=0x00ff00)
    BLUE = Colour(name="blue", rgb=(0, 0, 255), hexint=0x0000ff)
