import socket
import json

HOST_IP = "127.0.0.1"
PORT = 63337


class ClientConnection:
    def __init__(self, connection: "socket", address: str, client_id: int=None) -> None:
        self.connection = connection
        self.address = address
        self.client_id = client_id
        self.reply_in = b""
        self.reply_out = b""

    def send(value: str | bytes) -> None:
        if (type(value) is str):
            value = str.encode(value)
        self.connection.send(value)
        self.reply_out = value

    def sendall(value: str | bytes) -> None:
        if (type(value) is str):
            value = str.encode(value)
        self.connection.sendall(value)
        self.reply_out = value

    def receive(size: int) -> str:
        self.reply_in = self.connection.recv
        return self.reply_in.decode("utf-8")

    @staticmethod
    def wait_for_client(
            server: "socket",
            client_id: int=None) -> "ClientConnection":
        # Block until a client connects
        connection, address = server.accept()
        return ClientConnection(connection, address, client_id)


def handle_client_thread(client: ClientConnection) -> None:
    with client.connection:
        print(f"Connected at {client.address}")
        client.send(str.encode(f"Connected to: {HOST_IP}: {PORT}"))
        while True:
            # Recieve client data (bytes)
            data = client.receive(2048)
            if not data:
                print(f"Client {client['name']} disconnected")
                break
            connection.sendall(str.encode(response))

def main():
    # Bind socket with corresponding address type and socket tupe (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Connect specific network interface port
        server.bind((HOST_IP, PORT))

        # Enables incoming connections
        server.listen()
        print(f"Listening on {HOST_IP}:{PORT}...")

        client_one = ClientConnection.wait_for_client(server)
        if client_one:
            print("Client 1 connected")
        client_two = ClientConnection.wait_for_client(server)



if __name__ == "__main__":
    print("Attempting to start server...")
    main()
    print("Server stopped.")



