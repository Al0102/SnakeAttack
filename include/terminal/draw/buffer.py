"""
    An intermediary grid of cells to be displayed.
"""
from typing import Dict, Self, Tuple

from terminal.draw.cell import Cell


class RenderBuffer:
    def __init__(self, initial_state: Dict[Tuple[int, int], Cell] = None):
        if type(initial_state) is dict:
            self._cells: Dict[Tuple[int, int], Cell] = initial_state.copy()
        else:
            self._cells: Dict[Tuple[int, int], Cell] = {}
        
    def __len__(self) -> int:
        return len(self._cells)

    def write_cell(self, column: int, row: int, cell: Cell) -> None:
        self._cells[(column, row)] = cell
    
    def get_cell(self, column: int, row: int) -> Cell | None:
        return self._cells.get((column, row), " ")

    def clear(self) -> None:
        self._cells.clear()

    def clear_cell(self, column: int, row: int) -> None:
        if (column, row) in self._cells.keys():
            del self._cells[(column, row)]
    
    def copy(self) -> Self:
        return RenderBuffer(self._cells)
