from abc import ABC, abstractmethod
from enum import Enum, auto


class SCENE(Enum):
    FourOhFour = auto()
    QuitGame = auto()

    MainMenu = auto()
    SelectGameTypeMenu = auto()

    SnakeAttackPlay = auto()


class Scene(ABC):
    @staticmethod
    @abstractmethod
    def get_name() -> SCENE: ...

    def start(self) -> bool: ...

    @abstractmethod
    def update(self) -> SCENE: ...

    def end(self) -> bool: ...


class SceneSwitchType(Enum):
    # Change the current scene
    REPLACE = auto()
    # Open a new scene on the stack
    TOP = auto()
    # Close the current scene
    POP = auto()
    # Pop until specified scene
    STUMBLE = auto()

    NONE = auto()

