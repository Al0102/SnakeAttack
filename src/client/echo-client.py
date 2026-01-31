import socket
import threading

HOST_IP = "127.0.0.1"  # The host server's hostname/IP address
PORT = 65432  # The server's active port


def handle_input():
    while self.running:
        pressed = poll_key_press(key_in)
        try:
            choice = key_map[pressed]
        except KeyError:
            continue
        if choice == "q":
            break
    quit_game.set()


def start_game_loop(server):
    in_package = {
        "snakes": []}
    out_package = {
        "action_queue": []}

    threads = []
    t = threading.Thread(target=take_input)
    threads.append(t)
    t = threading.Thread(target=process_incoming, args=(server,))
    threads.append(t)

    clear_screen()
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()


# Bind socket with corresponding address type and socket tupe (TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Connect specific network interface port
    server.connect((HOST_IP, PORT))
    print(f"Searching for host on {HOST_IP}:{PORT}")

    # Send data to host
    server.sendall(b"Hello, world")

    # Receive data from host
    data = server.recv(1024)


print(f"Received {data!r}")
