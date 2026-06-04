# General
import sys
import time

# tGame
from terminal.screen import TerminalScreen
from terminal.input import KeyInput
from terminal.screen import TerminalScreen
from utils.types import Singleton

# Snake Attack
from game.root import Root
from game.scenes.scene_manager import SceneManager


class GameRoot(metaclass=Singleton):
    def __init__(self):
        # Config and instantiation
        Root()
        SceneManager(Root().settings.scene_main_entry)

        self.running = None

        # Signals
        Root().quit_game_signal.connect(self.stop)

    def start(self) -> int:
        self.running = True
        self.status = None
        with (TerminalScreen(),
              SceneManager() as scene_manager,
                KeyInput() as key_in):
            _run_result = self._run(scene_manager, key_in)
            return _run_result if self.status is None else self.status

    def stop(self, status: int = 0) -> int:
        if not self.running:
            raise RuntimeError(
                "Invalid GameRoot.stop() call, not started yet.\n"
                f"Try running {self}.start() first.")
        self.status = status
        self.running = False

    def _run(self, scene_manager: SceneManager, key_in: KeyInput) -> int:
        while self.running:
            # Input
            key_in.get_key()
            # Scene handling
            scene_manager.update()


def main(*args):
    with TerminalScreen():
        TerminalScreen.clear()
    game = GameRoot()
    status = game.start()

    # Post game printing
    # Newline and carriage return
    print()
    # Debugging
    if "--debug" in args:
        print("Status:", status)


if __name__ == "__main__":
    main(*sys.argv)
