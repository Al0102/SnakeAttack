# General
from typing import Dict, Any
import socket

# tGame
from ansi_actions.style import style, Style
from terminal.draw import create_text_area, draw_text_box
from terminal.screen import clear_screen

# Snake attack
from client.client_net import Client
from game.scenes.scene import Scene, SCENES
from game.snake import draw

class SnakeAttackPlay(Scene):
    def __init__(self):
        self.client = Client()
        self.game_state = None

    def start(self) -> Scene | None:
        clear_screen()
        try:
            data = self.client.connect()
            self.client.send("waiting")
        # TODO: replace with actual exceptions and a proper error screen
        except Exception:
            return SCENES.FourOhFour
        else:
            return

    def update(self, key_press: str) -> Scene | None:
        data = self.client.send(key_press)
        if data is None:
            # TODO: Connection Lost
            return SCENES.FourOhFour
        if data == "kick":
            self.client.send("acknowledged_kick", receive=False)
            return SCENES.MainMenu
        self.game_state = data
        if not self.game_state:
            return
        if type(self.game_state) is dict:
            draw(self.game_state["snake"]["segments"])



