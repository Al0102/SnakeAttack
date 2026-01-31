import socket
import json

HOST_IP = "127.0.0.1"
PORT = 65432


# TODO Take multiple actions if longer than deltaT (or certain length of actions) from queue
def process_input(data):
    pass


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


    clients = []
    while len(clients) < 2:
        clients.append(wait_for_client(server))
        print(f"{len(clients)}/3 connected")
        for client_id, client in enumerate(clients):
            data = client["connection"].recv(1024)
            client["connection"].sendall(f"{client_id + 1}/3 connected".encode("utf-8"))
    print("Starting...")

    for client_id, client in enumerate(clients):
        with client["connection"]:
            print(f"Connected at {client['address']}")

#    while True:
#        # Recieve client data (bytes)
#
#        # Empty bytes object siginifying client disconnect
#        if not data:
#            break
#
#        # Send data to client (bytes)
#        connection.sendall(data)

print("Server stopped.")
