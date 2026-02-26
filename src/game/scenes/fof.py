from ansi_actions.style import style, Style
from terminal.draw import create_text_area, draw_text_box
from terminal.screen import get_screen_size, clear_screen

from scenes import Scene, SCENES

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
        return SCENES.MainMenu

