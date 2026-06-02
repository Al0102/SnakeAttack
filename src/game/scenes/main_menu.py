# General
from typing import Dict, Any

# tGame
from ansi_actions.style import style, Style
from terminal.input import KeyInput
from terminal.screen import get_screen_size
from terminal.draw import create_text_area, draw_text_box
from terminal.menu import Menu

# Snake attack
from game.root import Root
from game.scenes.scene import Scene, SCENE, SceneSwitchType


class MainMenu(Scene):
    OPTIONS = (
        "START",
        "SETTINGS",
        "QUIT")

    def __init__(self) -> None:
        super().__init__()
        self.menu: Menu = Menu(
            2, (get_screen_size()[1] - len(MainMenu.OPTIONS) - 2),
            *MainMenu.OPTIONS)

        self.title: Dict[str, Any] = create_text_area(
            column=2, row=(get_screen_size()[1] - len(MainMenu.OPTIONS) - 4),
            width=13, height=1,
            text=style("Snake Attack!",
                  Style.GREEN, Style.UNDERLINE, Style.BOLD, Style.SLOW_BLINK))

    @staticmethod
    def get_name():
        return SCENE.MainMenu

    def start(self) -> None:
        self.menu.reset_option()
        self.menu.draw_menu()
        draw_text_box(text_area=self.title, overwrite=True)

    def update(self) -> Scene | None:
        _key_press = KeyInput().pull_key()
        if not _key_press:
            return None

        # Get next scene
        _choice = self.menu.update_menu(_key_press)
        match _choice:
            case "START":
                Root().switch_scene(SceneSwitchType.TOP, SCENE.FourOhFour)
            case "SETTINGS":
                Root().switch_scene(SceneSwitchType.TOP, SCENE.FourOhFour)
            case "QUIT":
                Root().switch_scene(SceneSwitchType.TOP, SCENE.QuitGame)
            case _:
                return None

    def end(self):
        return super().end()

