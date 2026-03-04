from game.snake_attack_host import SnakeAttackState
import time


class SnakeAttackHost:
    FPS = 2
    def __init__(self, clients):
        self.clients = clients
        self.client_one = clients[0]["handler"]
        self.client_two = clients[1]["handler"]

        self.game_state = SnakeAttackState(
                clients[0]["client"].client_id,
                clients[1]["client"].client_id)

        self.running = False

    def start_game(self):
        self.running = True
        current_time = time.time()
        previous_time = current_time
        
        self.client_one.stop()
        self.client_two.stop()

        self.client_one.set_thread(
                self.client_one.handle_game_as_snake,
                target_args=(self.game_state,))

        self.client_two.set_thread(self.client_two.handle_kick)
        self.client_two.run()

        self.client_one.run()
        while self.game_state.running:
            previous_time = current_time
            current_time = time.time()
            delta_t = current_time - previous_time

            if delta_t < SnakeAttackHost.FPS:
                time.sleep(SnakeAttackHost.FPS - delta_t)

            self.game_state.update()
        self.client_one.stop()

    def clean_up(self):
        self.client_one.stop()

        self.client_one.set_thread(self.client_one.handle_kick)
        self.client_one.run()

