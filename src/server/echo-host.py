import time 
import socket
import pickle
from threading import Thread, Lock
from typing import Callable, Any, Dict

from ansi_actions.cursor import cursor_set, cursor_shift, set_cursor_visibility
from ansi_actions.style import style, Style
from terminal.screen import clear_screen, get_screen_size

from snake_attack_server import SnakeAttackHost

HOST_IP = "127.0.0.1"
PORT = 63337


class ClientConnection:
    def __init__(self, connection: "socket", address: str, client_id: int=None) -> None:
        self.connection = connection
        self.connected = True
        self.address = address
        self.client_id = client_id
        self.reply_in = b"None"
        self.reply_out = b"None"

    def is_active(self) -> bool:
        return self.connected and bool(self.reply_in)

    def set_disconnected(self) -> None:
        self.connected = False

    def close(self) -> None:
        self.connection.close()
        self.set_disconnected()

    def send(self, value: str | bytes) -> None:
        if (type(value) is str):
            value = str.encode(value)
        self.connection.send(value)
        self.reply_out = value

    def sendall(self, value: str | bytes) -> None:
        if (type(value) is str):
            value = str.encode(value)
        self.connection.sendall(value)
        self.reply_out = value

    def receive(self, size: int, as_string: bool=True) -> str:
        self.reply_in = self.connection.recv(size)
        if not self.reply_in:
            self.set_disconnected
        if as_string:
            return self.reply_in.decode("utf-8")
        else:
            return self.reply_in

    @staticmethod
    def wait_for_client(
            server: "socket",
            client_id: int=None) -> "ClientConnection":
        # Block until a client connects
        connection, address = server.accept()
        return ClientConnection(connection, address, client_id)


class ClientHandler:
    def __init__(self, client: ClientConnection) -> None:
        self.client = client
        self.thread = None
        self.running = False

    def set_client(self, client: ClientConnection) -> bool:
        if client is None or \
                not type(client) is ClientConnection or \
                (self.thread is not None and self.thread.is_alive()):
            return False
        self.client = client
        self.thread = Thread(target=self.handle_client_thread, args=(client,))
        return True
    
    def run(self) -> None:
        print(style("Running", Style.GREEN))
        if self.thread and not self.thread.is_alive():
            self.running = True
            self.thread.start()

    def stop(self) -> None:
        if self.thread and self.thread.is_alive():
            self.running = False
            self.thread.join()

    def set_thread(
            self,
            thread_target: Callable,
            target_args: tuple=()) -> None:
        self.thread = Thread(target=thread_target, args=target_args)

    def handle_kick(self) -> int:
        print(f"Kicking client {self.client.client_id}...")
        while self.running:
            print("doing kick")
            data = self.client.receive(2048, as_string=False)
            if not data or pickle.loads(data) == "acknowledged_kick":
                print(f"Kicked client {self.client.client_id}...")
                self.client.close()
                self.running = False
                break
            self.client.sendall(pickle.dumps("kick"))

    def handle_waiting(self, clients: Dict[int, Dict[str, Any]]) -> int:
        print(f"Client: {self.client.client_id} connected.")
        while self.running:
            # Recieve client data (bytes)
            data = self.client.receive(2048, as_string=False)
            if not self.client.is_active():
                print(f"Client {self.client.client_id} disconnected")
                return 2
            self.client.sendall(pickle.dumps(f"{len(clients)}/2 connected"))

    def handle_game_as_snake(self, game) -> int:
        print(f"Starting game, Player: {self.client.client_id} connected.")
        data = self.client.receive(2048, as_string=False)
        self.client.send(pickle.dumps("start_game"))
        while self.running:
            # Recieve client data (bytes)
            data = self.client.receive(2048, as_string=False)
            if not self.client.is_active():
                print(f"Client {self.client.client_id} disconnected")
                return 2
            data = pickle.loads(data)
            print(f"Received '{data}' from {self.client.client_id}")

            game.try_player_update(self.client.client_id, data).join()
            self.client.sendall(pickle.dumps(game.get_state()))
        print("Left normally")
        return 0


# Start main

grail = False
grail_lock = Lock()
stop_server = False
def check_disconnects(clients: Dict[int, Dict[str, Any]]) -> None:
    global grail
    while not stop_server:
        to_remove = set()
        for client_id, client in list(clients.items()):
            status_message = \
                f"Status: Client {client_id}, {client['client'].is_active()}"
#            cursor_set(
#                    get_screen_size()[0] - len(status_message),
#                    2 + client_id % 2)
            #print(status_message)
            if not client["client"].is_active():
                grail = True
                to_remove.add(client_id)
        for client_id in to_remove:
            update_client_status(clients, client_id, False)

def update_client_status(
        clients: Dict[int, Dict[str, Any]],
        client_id: int,
        add_pop: bool,
        connection: socket.socket | None=None) -> None:
    with grail_lock:
        if add_pop:
            if connection is None:
                return
            new_client = {
                    "client": connection
            }
            print(f"Client {client_id} connected")
            new_client["handler"] = ClientHandler(new_client["client"])
 #            new_client["handler"].set_thread(
 #                    new_client["handler"].handle_waiting_for_players)
            #new_client["handler"].run()
            clients[client_id] = new_client
        else:
            clients[client_id]["handler"].stop()
            clients[client_id]["client"].set_disconnected()


def main():
    global stop_server
    # Bind socket with corresponding address type and socket tupe (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        retry = 1
        while True:
            try:
                # Connect specific network interface port
                time.sleep(2)
                server.bind((HOST_IP, PORT))
            except OSError:
                print(f"{HOST_IP}:{PORT} in use")
                if retry > 5:
                    print("Continue trying? (yes/[else])")
                    if input() != "yes":
                        return
                    retry = 1
                print(f"Attempt {retry}/5")
                retry += 1
            else:
                break

        # Enables incoming connections
        server.listen()
        print(f"Listening on {HOST_IP}:{PORT}...")

        # Start connecting clients
        clients = {}
        current_id = 0

        t = Thread(target=check_disconnects, args=(clients,))
        t.start()

        while len(clients) != 2:
            print(f"Connected clients: {len(clients)}")
            update_client_status(
                    clients, current_id, True,
                    ClientConnection.wait_for_client(server, current_id))
            clients[current_id]["client"].send(
                    f"You connected to {HOST_IP}:{PORT}")
            clients[current_id]["handler"].set_thread(
                clients[current_id]["handler"].handle_waiting,
                target_args=(clients,))
            clients[current_id]["handler"].run()
            current_id = (current_id + 1) % 2

        clear_screen()
        #cursor_shift("left", get_screen_size()[0])
        print(style("Starting...", Style.GREEN))

        game_host = SnakeAttackHost(clients)
        try:
            game_host.start_game()
        except Exception as e:
            stop_server = True
            t.join()
            print("I'm erroring")
            print(style(str(e), Style.RED))
            return e
        
        game_host.clean_up()

        stop_server = True
        t.join()

        for client in clients.values():
            if client["handler"].thread.is_alive():
                client["handler"].thread.join()
                client["handler"].stop()

        return "Success"


if __name__ == "__main__":
    clear_screen()
    set_cursor_visibility(False)
    print("Attempting to start server...")
    error = main()
    print(error)
    print("Server stopped.")
    set_cursor_visibility(True)




