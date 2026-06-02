from enum import Enum, auto
from typing import Dict

from utils.types import Singleton

from game.root import Root
from game.scenes.fof import FourOhFour
from game.scenes.main_menu import MainMenu
from game.scenes.root import QuitGame
from game.scenes.scene import Scene, SCENE, SceneSwitchType
from game.scenes.snake_attack import SnakeAttackPlay


class SceneManager(metaclass=Singleton):
    SCENES: Dict[SCENE, Scene] = {
        SCENE.MainMenu: MainMenu,
        SCENE.FourOhFour: FourOhFour,
        SCENE.QuitGame: QuitGame,
        SCENE.SnakeAttackPlay: SnakeAttackPlay
    }

    def __init__(self, entry_scene: SCENE = SCENE.MainMenu):
        Root().scene_switch_signal.connect(self.switch)
        
        self._active = [SceneManager.SCENES[entry_scene]()]

        self._next_scene = None
        self._switch_type: SceneSwitchType = None

    def __enter__(self):
        self._current().start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._current().end()

    def update(self) -> None:
        self._current().update()
        if self._switch_type:
            match self._switch_type:
                case SceneSwitchType.REPLACE:
                    self._replace_current()
                case SceneSwitchType.TOP:
                    self._top_current()
                case SceneSwitchType.POP:
                    self._pop_current()
                case SceneSwitchType.STUMBLE:
                    self._stumble_current()
            self._reset_queue()

    def switch(self, switch_type: SceneSwitchType, next_scene: SCENE = None) -> None:
        if next_scene in SceneManager.SCENES or switch_type == SceneSwitchType.POP:
            self._next_scene = next_scene
            self._switch_type = switch_type

    def _current(self) -> Scene:
        return self._active[-1]

    def _reset_queue(self) -> None:
        self._switch_type = None
        self._next_scene = None

    def _replace_current(self) -> None:
        self._current().end()
        self._active[-1] = SceneManager.SCENES[self._next_scene]()
        self._current().start()

    def _top_current(self) -> None:
        self._active.append(SceneManager.SCENES[self._next_scene]())
        self._current().start()

    def _pop_current(self) -> None:
        if len(self._active) > 1:
            self._current().end()
            self._active.pop()

    def _stumble_current(self) -> None:
        _curr_scene = None
        while len(self._active) > 1 and _curr_scene != self._next_scene:
            self._pop_current()
            _curr_scene = self._current().get_name()

