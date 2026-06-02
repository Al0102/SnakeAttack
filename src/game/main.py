# General
import sys
import time

# tGame
from terminal.screen import clear_screen
from terminal.input import KeyInput
from utils.types import Singleton

# Snake Attack
from game.root import Root
from game.scenes.scene_manager import SceneManager


class GameRoot(metaclass=Singleton):
    def __init__(self):
        # Config and instantiation
        Root()
        SceneManager(self.settings.scene_main_entry)
        self.running = True

    def run(self) -> int:
        with (SceneManager() as scene_manager,
                KeyInput() as key_in):
            while self.running:
                # Input
                key_in.get_key()
                # Scene handling
                scene_manager.update()


def main(*args):
    clear_screen()
    game = GameRoot()
    game.run()
    clear_screen()


if __name__ == "__main__":
    main(*sys.argv)
