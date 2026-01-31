import socket

HOST_IP = "127.0.0.1"
PORT = 63337

# Bind socket with corresponding address type and socket tupe (TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Connect specific network interface port
    server.bind((HOST_IP, PORT))

    # Enables incoming connections
    server.listen()
    print(f"Listening on {HOST_IP}:{PORT}...")

    # Block until a client connects
    connection, address = server.accept()

    with connection:
        print(f"Connected at {address}")
        connection.send(str.encode(f"Connected to: {HOST_IP}: {PORT}"))
        while True:
            # Recieve client data (bytes)
            data = connection.recv(2048)

            # Empty bytes object siginifying client disconnect
            if not data:
                break

            # Send data to client (bytes)
            connection.sendall(data)

print("Server stopped.")
