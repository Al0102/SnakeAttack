from ansi_actions.style import style, Style
from terminal.menu import create_menu, get_centered_menu_position
from terminal.draw import create_text_area, draw_text_box
from terminal.screen import get_screen_size, clear_screen
from terminal.input import init_key_input, poll_key_press
from client.client_net import Client

from typing import Dict, Any


class Scene:
    def __init__(self):
        pass


class QuitGame(Scene):
    def __init__(self):
        pass


class FourOhFour(Scene):
    def __init__(self) -> None:
        scene_not_found_message = "404 Scene not found"
        instructions_message = "Press any key to return to main menu"
        self.instructions: Dict[str, Any] = create_text_area(
            *get_centered_menu_position(
                scene_not_found_message,
                instructions_message),
            32, 2,
            style(scene_not_found_message, Style.RED) + "\n" +
            style(instructions_message,
                  Style.YELLOW, Style.RAPID_BLINK))

        self.just_entered = True

    def update(self, key_press: str) -> Scene | None:
        clear_screen()
        draw_text_box(text_area=self.instructions, flush_output=True)
        if self.just_entered:
            self.just_entered = False
            return None
        return MainMenu()


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
                return FourOhFour()
            case "SETTINGS":
                return FourOhFour()
            case "QUIT":
                return QuitGame()
            case _:
                return None


class Game:
    def __init__(self):
        self.current_scene = MainMenu()
        self.running = True

        self.key_input = init_key_input()

        self.client = None

    def start_loop(self):
        while self.running:
            # Get input
            pressed = poll_key_press(self.key_input)
            if pressed == "q":
                break

            # Scene handling
            next_scene = self.current_scene.update(pressed)
            if not next_scene:
                continue

            if type(next_scene) == QuitGame:
                break
            else:
                self.current_scene = next_scene


    def attempt_connection(self):
        self.client = Client()


def main():
    clear_screen()
    game = Game()
    game.start_loop()


if __name__ == "__main__":
    main()
