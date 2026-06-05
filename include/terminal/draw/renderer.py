"""
    Handler for window buffers when displaying to the screen.
"""

import sys
from typing import Dict, List, Self, Tuple

from ansi_actions.cursor import cursor_set_ansii, cursor_shift_ansii
from terminal.draw.buffer import RenderBuffer
from terminal.draw.cell import Cell
from terminal.draw.colour import Colour, Colours
from terminal.screen import TerminalScreen
from utils.utilities import Direction


class _RendererConstants:
    """
    The minimum number of cells between row changes before a jump is made.
    """
    JUMP_THRESHOLD: int = 8


class Renderer:
    def __enter__(self) -> Self:
        self._store_buffer = RenderBuffer()
        self._edit_buffer = RenderBuffer()
        return self

    def __exit__(self, _, __, traceback) -> None:
        """
        Prints errors with manager.
        """
        if traceback:
            print(traceback, file=sys.stderr)

    def write(self, column: int, row: int, cell: Cell) -> None:
        self._edit_buffer.write_cell(column, row, cell)

    def writes(self, cell_group: Dict[Tuple[int, int], Cell]) -> None:
        for position, cell in cell_group.items():
            self._edit_buffer.write_cell(*position, cell)
    
    def write_line(
            self,
            column: int, row: int,
            line: str,
            front_colour: Colour = Colours.NONE,
            back_colour: Colour = Colours.NONE) -> None:
        for offset, character in enumerate(line):
            _cell = Cell(character, front_colour, back_colour)
            self.write(column + offset, row, _cell)
    
    def wipe(self) -> None:
        self._store_buffer.clear()
        self._edit_buffer.clear()

    def flush(self) -> None:
        if len(self._store_buffer) == 0:
            TerminalScreen.clear()
        _output_string = ""
        _changed = self._diff()
        for row, change_row in _changed.items():
            _changes = sorted(change_row, key=lambda change: change[0])
            _output_string += cursor_set_ansii(max(1, _changes[0][0]), row)
            _previous_x = _changes[0][0]
            for column, cell in _changes:
                if not all(TerminalScreen.check_is_inside((column, row))):
                    self._store_buffer.write_cell(column, row, cell)
                    continue
                _jump = column - max(1, _previous_x)
                if _jump > _RendererConstants.JUMP_THRESHOLD and False:
                    _output_string += cursor_shift_ansii(Direction.RIGHT, _jump)
                    _output_string += str(cell)
                else:
                    for old_column in range(max(1,_previous_x + 1), column):
                        _output_string += str(self._store_buffer.get_cell(old_column, row))
                    _output_string += str(cell)
                _previous_x = column
                self._store_buffer.write_cell(column, row, cell)
        print(_output_string, end="", flush=True)
        self._edit_buffer.clear()

    def save(self) -> RenderBuffer:
        return self._store_buffer.copy()
    
    def restore(self, buffer: RenderBuffer):
        self._edit_buffer.clear()
        self._edit_buffer = buffer
        self.flush()

    def _diff(self) -> Dict[int, List[Tuple[int, Cell | None]]]:
        """
        Rows of changes as output.
        """
        _changes = {}
        for (column, row), cell in self._edit_buffer._cells.items():
            if cell != self._store_buffer.get_cell(column, row):
                _changes.setdefault(row, []).append((column, cell))
        return _changes