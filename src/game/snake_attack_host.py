import threading
from typing import Any, Dict

from utils.utilities import Direction

from game.snake import Snake, convert_snake_to_json_dict
from game.player import Player


class SnakeAttackState:
    def __init__(self, player_one_id: int, player_two_id: int):
        self.snake = Snake((2, 2))
        self.p_one = Player(player_one_id)
        self.p_two = Player(player_two_id)
        self.thread_lock = threading.Lock()
        self.running = True

    def get_state(self) -> Dict[str, Any]:
        return {
            "snake": convert_snake_to_json_dict(self.snake),
            "status": self.running}

    def update(self):
        self.snake.move()

    def try_player_update(self, p_id: int, data: Any) -> None:
        update_thread = threading.Thread(
                target=self.player_update,
                args=(p_id, data))
        update_thread.start()
        return update_thread

    def player_update(self, p_id: int, data: Any) -> None:
        with self.thread_lock:
            if p_id == 0:
                value = self.p_one.key_map.get(data)
                if value == "quit":
                    self.running = False
                else:
                    try:
                        new_direction = Direction(value)
                    except ValueError:
                        # TODO: raise something bc invalid input
                        pass
                    else:
                        self.snake.set_facing(new_direction)



