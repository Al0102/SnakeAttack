from typing import Dict
from utils.utilities import Direction

from game.scenes.scene import SCENE


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

    # Scenes
    SCENE_MAIN_ENTRY = SCENE.MainMenu

    # Frames
    DEFAULT_FPS = 30


    def __init__(
            self,
            action_map: Dict[str, tuple] = DEFAULT_ACTION_MAP,
            scene_main_entry: SCENE = SCENE_MAIN_ENTRY,
            fps: int = DEFAULT_FPS
    ):
        self.action_map = action_map
        self.scene_main_entry = scene_main_entry
        self.fps = fps

