import socket
import json

HOST_IP = "127.0.0.1"
PORT = 63337


def wait_for_client(server):
    # Block until a client connects
    connection, address = server.accept()
    return { "connection": connection, "address": address}


# Bind socket with corresponding address type and socket tupe (TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Connect specific network interface port
    server.bind((HOST_IP, PORT))

    # Enables incoming connections
    server.listen()
    print(f"Listening on {HOST_IP}:{PORT}...")


    with connection:
        print(f"Connected at {address}")
        connection.send(str.encode(f"Connected to: {HOST_IP}: {PORT}"))
        while True:
            # Recieve client data (bytes)
            data = connection.recv(2048)
            if not data:
                break
            connection.sendall(str.encode("--reply--"))


print("Server stopped.")
