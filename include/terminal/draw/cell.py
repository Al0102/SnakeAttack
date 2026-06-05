"""
    A single cell/pixel/tile/character on the terminal.
"""
from dataclasses import dataclass

from ansi_actions.style import style, style_raw
from terminal.draw.colour import Colour, Colours


@dataclass(frozen=True)
class Cell():
    character: str
    front_colour: Colour = Colours.NONE
    back_colour: Colour = Colours.NONE

    def __str__(self):
        return style_raw(
            self.character,
            self.front_colour.front(),
            self.back_colour.back())
