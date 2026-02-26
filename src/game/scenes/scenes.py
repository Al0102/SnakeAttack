from enum import Enum, auto

class Scene:
    def __init__(self):
        pass

class SCENES(Enum):
    FourOhFour = auto()
    QuitGame = auto()

    MainMenu = auto()
    SelectGameTypeMenu = auto()

    SnakeAttackPlay = auto()
