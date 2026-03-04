from typing import Dict
from enum import Enum

from utils.utilities import Direction


class Player:
    DEFAULT_KEY_MAP = {
        "w": Direction.UP,
        "s": Direction.DOWN,
        "a": Direction.LEFT,
        "d": Direction.RIGHT,
        "tab": "quit",
        "a": "grow"}

    def __init__(
            self,
            player_id: int,
            key_map: Dict[str, Direction]=None) -> None:
        self.id = player_id
        if key_map:
            self.key_map = key_map
        else:
            self.key_map = Player.DEFAULT_KEY_MAP

    def get_id() -> int:
        return self.player_id


