from typing import Dict

from utils.signal import Signal
from utils.types import Singleton

from game.scenes.scene import SCENE, SceneSwitchType
from game.settings import Settings


class Root(metaclass=Singleton):
    def __init__(self):
        self.settings = Settings()

        self._init_signals()

    def switch_scene(
        self,
        switch_type: SceneSwitchType = SceneSwitchType.REPLACE,
        scene: SCENE = None
    ) -> None:
        self.scene_switch_signal.emit(switch_type, scene)

    def quit(self, status: int=0) -> None:
        self.quit_game_signal.emit(status)

    def _init_signals(self):
        self.scene_switch_signal = Signal(SceneSwitchType, SCENE)
        self.quit_game_signal = Signal(int)