from ansi_actions.style import style
from ansi_actions import cursor
from terminal.screen import clear_screen
from terminal.input import init_key_input, get_key_codes, poll_key_press
from utils.utilities import LinkedNode, Direction, get_direction_vectors

from typing import Dict, Tuple, Set
from enum import Enum
import threading
import time


class Segment(LinkedNode):
    def __init__(self, position: Tuple[int, int], next_node: "Segment"=None) -> None:
        super().__init__(position, next_node)

    def get_position(self) -> Tuple[int, int]:
        return self.value

    def set_position(self, new_position: Tuple[int, int]) -> None:
        if not (type(new_position) is tuple and len(new_position) == 2):
            raise TypeError(style("new_position must be a Vector2 (Tuple[int, int]), "
                            f"found {type(new_position)}: {new_position}", "red"))
        self.value = new_position

    def move(self, direction: Direction) -> None:
        if direction not in Direction:
            raise TypeError(style(f"direction be a Direction, found {direction}", "red"))
        displacement = get_direction_vectors()[direction]
        current_position = self.get_position()
        self.set_position((
                current_position[0] + displacement[0], # x position
                current_position[1] + displacement[1])) # y position


class Snake:
    def __init__(self, position: Tuple[int, int], butt_segment: Segment=None, initial_length: int=3) -> None:
        # Segments init
        if not butt_segment:
            self.butt = Segment(position=position, next_node=None)
            for segment in range(initial_length - 1):
                self.add_segment()
        else:
            self.butt = butt_segment

        # Initial direction of head
        self.facing = Direction.RIGHT

        # Initial state
        self.dead = False

    def get_segments(self):
        segments = []
        segment = self.butt
        while segment is not None:
            segments.append(segment)
            segment = segment.next
        return segments

    def add_segment(self) -> None:
        new_butt = Segment(self.butt.get_position(), self.butt)
        self.butt = new_butt

    def move(self) -> None:
        positions: Set[Tuple[int, int]] = {}
        segment: Segment = self.butt
        while True:
            # Snake body handling
            if segment.next != None:
                segment.set_position(segment.next.get_position())
                segment = segment.next
                continue

            # Snake head handling
            segment.move(self.facing)

            # Check collide
            # TODO: move to main game loop
            if segment.get_position() in positions:
                self.dead = True
            break


key_map: Dict[str, str] = {
    "up": Direction.UP,
    "down": Direction.DOWN,
    "left": Direction.LEFT,
    "right": Direction. RIGHT,
    "tab": "q"
}


def draw(snake: Snake) -> None:
    clear_screen()
    for seg in map(lambda x: x.get_position(), snake.get_segments()):
        cursor.cursor_set(seg[0], seg[1])
        print(style("o", "green"), end="")
    print("", end="", flush=True)


quit_game = threading.Event()
choice = None


def tick_snake(snake):
    while not quit_game.is_set():
        time.sleep(0.5)
        snake.move()
        draw(snake)


def handle_game(snake):
    while not quit_game.is_set():
        # Handle input
        if choice == None:
            continue
        if choice == "q":
            break

        # Handle updates
        snake.facing = choice
        if snake.dead:
            print(style("Dead", "red"))
            break
    quit_game.set()


def handle_input():
    global choice
    key_in = init_key_input()
    while not quit_game.is_set():
        pressed = poll_key_press(key_in)
        try:
            choice = key_map[pressed]
        except KeyError:
            continue
        if choice == "q":
            break
    quit_game.set()


def main():
    snake = Snake((2, 2))

    # Start threads for input and game logic
    threads = []

    t = threading.Thread(target=handle_input)
    threads.append(t)
    t = threading.Thread(target=handle_game, args=(snake,))
    threads.append(t)
    t = threading.Thread(target=tick_snake, args=(snake,))
    threads.append(t)

    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()


if __name__ == "__main__":
    cursor.set_cursor_visibility(False)
    main()
    cursor.set_cursor_visibility(True)
