# General

# tGame
from terminal.screen import clear_screen

# Snake attack
from client.client_net import Client
from game.scenes.scene import Scene, SCENE

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
            return SCENE.FourOhFour
        else:
            return

    def update(self, key_press: str) -> Scene | None:
        data = self.client.send(key_press)
        if data is None:
            # TODO: Connection Lost
            return SCENE.FourOhFour
        if data == "kick":
            self.client.send("acknowledged_kick", receive=False)
            return SCENE.MainMenu
        self.game_state = data
        if not self.game_state:
            return
        if type(self.game_state) is dict:
            (self.game_state["snake"]["segments"])



