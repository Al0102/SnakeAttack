from typing import Dict
from utils.utilities import Direction


class Settings:
    """
    Default ACTION : KEY mapping.
    """
    DEFAULT_ACTION_MAP: Dict[str, tuple] = {
        "ui_up": ("up", "w"),
        "ui_down": ("down", "s"),
        "ui_left": ("left", "a"),
        "ui_right": ("right", "d"),

        "move_up": ("up", "w"),
        "move_down": ("down", "s"),
        "move_left": ("left", "a"),
        "move_right": ("right", "d"),

        "cheat_grow": "+",

        "force_quit": "4",
    }

