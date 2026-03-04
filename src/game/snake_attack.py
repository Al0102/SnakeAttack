from ansi_actions.style import style, Style
from terminal.menu import create_menu, get_centered_menu_position
from terminal.draw import create_text_area, draw_text_box
from terminal.screen import get_screen_size, clear_screen
from terminal.input import init_key_input, poll_key_press
from client.client_net import Client

from game.scenes.scene import Scene, SCENES
from game.scenes.main_menu import MainMenu
from game.scenes.fof import FourOhFour 
from game.scenes.root import QuitGame 
from game.scenes.snake_attack import SnakeAttackPlay

class Game:
    SCENES: Dict[int, Scene] = {
        SCENES.MainMenu: MainMenu,
        SCENES.FourOhFour: FourOhFour,
        SCENES.QuitGame: QuitGame,
        SCENES.SnakeAttackPlay: SnakeAttackPlay

    }

    def __init__(self):
        self.current_scene = Game.SCENES[SCENES.MainMenu]()
        self.running = True

        self.key_input = init_key_input()
        self.pressed = []

    def start_loop(self):
        while self.running:
            # Get input
            pressed = poll_key_press(self.key_input)
            if pressed == "q":
                break
            # Scene handling
            self.current_scene.start()
            next_scene = self.current_scene.update(pressed)
            if not next_scene:
                continue
            self.current_scene.end()
            if next_scene == SCENES.QuitGame:
                break
            elif next_scene in Game.SCENES.keys():
                self.current_scene = Game.SCENES[next_scene]()
            else:
                self.current_scene = Game.SCENES[SCENES.FourOhFour]()


def main():
    clear_screen()
    game = Game()
    game.start_loop()


if __name__ == "__main__":
    main()
