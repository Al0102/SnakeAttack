"""
    A single cell/pixel/tile/character on the terminal.
"""
from dataclasses import dataclass

from ansi_actions.style import style
from terminal.draw.colour import Colour


@dataclass
class Cell(frozen=True):
    character: str
    front_colour: Colour
    back_colour: Colour

    def __repr__(self):
        return style(
            self.character,
            self.front_colour.front(),
            self.back_colour.back())
