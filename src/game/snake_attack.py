from ansi_actions.style import style, Style
from terminal.menu import create_menu, get_centered_menu_position
from terminal.draw import create_text_area, draw_text_box
from terminal.screen import get_screen_size, clear_screen
from terminal.input import init_key_input, poll_key_press
from client.client_net import Client

from scenes.scenes import Scenem SCENES
from scenes import main_menu.MainMenu,
                   fof.FourOhFour,
                   root.QuitGame


class Game:
    SCENES: Dict[int, Scene] = {
        SCENES.MainMenu: main_menu.MainMenu,
        SCENES.FourOhFour: fof.FourOhFour,
        SCENES.QuitGame: root.QuitGame
    }

    def __init__(self):
        self.current_scene = Game.SCENES[SCENES.MainMenu]()
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
            if next_scene == SCENES.QuitGame:
                break
            elif next_scene in Game.SCENES.keys():
                self.current_scene = Game.SCENES[next_scene]()
            else:
                self.current_scene = Game.SCENES[SCENES.FourOhFour]()

    def attempt_connection(self):
        self.client = Client()


def main():
    clear_screen()
    game = Game()
    game.start_loop()


if __name__ == "__main__":
    main()
