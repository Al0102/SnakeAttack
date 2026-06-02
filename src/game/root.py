from typing import Dict

from utils.signal import Signal
from utils.types import Singleton

from game.scenes.scene import SCENE, SceneSwitchType
from game.settings import Settings


class Root(metaclass=Singleton):
    def __init__(self):
        self.scene_switch_signal = Signal(SceneSwitchType, SCENE)
        self.settings = Settings()

    def switch_scene(
        self,
        switch_type: SceneSwitchType = SceneSwitchType.REPLACE,
        scene: SCENE = None
    ):
        self.scene_switch_signal.emit(switch_type, scene)


