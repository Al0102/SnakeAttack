# General
from typing import Dict, Any

# tGame
from ansi_actions.style import style, Style
from terminal.draw import create_text_area, draw_text_box
from terminal.menu import create_menu

# Snake attack
from scenes import Scene, SCENES


class MainMenu(Scene):
    OPTIONS = (
        "START",
        "SETTINGS",
        "QUIT")
    def __init__(self) -> None:
        self.menu: Dict[str, callable] = create_menu(
            2, (get_screen_size()[1] - len(MainMenu.OPTIONS) - 2),
            *MainMenu.OPTIONS)

        self.title: Dict[str, Any] = create_text_area(
            column=2, row=(get_screen_size()[1] - len(MainMenu.OPTIONS) - 4),
            width=13, height=1,
            text=style("Snake Attack!",
                  Style.GREEN, Style.UNDERLINE, Style.BOLD, Style.SLOW_BLINK))

    def update(self, key_press: str) -> Scene | None:
        clear_screen()
        draw_text_box(text_area=self.title)
        choice = self.menu["update_menu"](key_press)
        match choice:
            case "START":
                return SCENES.FourOhFour
            case "SETTINGS":
                return SCENES.FourOhFour
            case "QUIT":
                return SCENES.QuitGame
            case _:
                return None

