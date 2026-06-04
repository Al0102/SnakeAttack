# Other
from typing import Any, Dict

# tGame
from ansi_actions.style import reset_style, style, Style
from terminal.input import KeyInput
from terminal.menu import get_centered_menu_position
from terminal.draw import create_text_area, draw_text_box
from terminal.screen import TerminalScreen

# SnakeAttack
from game.root import Root
from game.scenes.scene import Scene, SCENE, SceneSwitchType


class FourOhFour(Scene):
    def __init__(self) -> None:
        scene_not_found_message = "404 Scene not found"
        instructions_message = "Press any key to return to main menu"
        self.instructions: Dict[str, Any] = create_text_area(
            *get_centered_menu_position(
                scene_not_found_message,
                instructions_message),
            len(instructions_message), 2,
            style(scene_not_found_message, Style.RED) + "\n" +
            style(instructions_message,
                  Style.YELLOW, Style.RAPID_BLINK))

        self.just_entered = True

    @staticmethod
    def get_name():
        return SCENE.FourOhFour

    def start(self) -> None:
        TerminalScreen.clear()
        draw_text_box(text_area=self.instructions, flush_output=True)
        return super().start()

    def update(self) -> SCENE | None:
        _key = KeyInput().get_key()
        if self.just_entered and _key:
            self.just_entered = False
            return None
        Root().switch_scene(SceneSwitchType.POP)
        return SCENE.MainMenu

    def end(self) -> None:
        TerminalScreen.clear()
        reset_style()
        return super().end()
