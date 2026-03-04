from ansi_actions.style import Style, style

from sys import stderr
import socket
import pickle
from typing import Any


class Client:
    DEFAULT_HOST_IP = "127.0.0.1"
    DEFAULT_PORT = 63337

    def __init__(self, ip: str=DEFAULT_HOST_IP, port: int=DEFAULT_PORT, debug: bool=False):
        """
        Initialize a Client connection entity.

        :param ip: (default Client.DEFAULT_HOST_IP) a string representing the host IP address to connect to
        :param port: (default Client.DEFAULT_PORT) an integer representing the port of the connection
        :param debug (default False): a boolean representing whether to print errors
        """
        self.server_ip: str = ip
        self.port: int = port

        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr: Tuple[str, int] = (self.server_ip,  self.port)
        self.debug: bool = debug

    def connect(self) -> str | None:
        """
        Establish a connection to the host server.

        :precondition: [client & addr] must be initialized
        :postcondition: return a reply from the host or None if an error occurred while connecting
        :return: a string representing the reply from the host,
                 or None if an error occurred while connecting
        """
        try:
            self.client.connect(self.addr)
        except Exception as connection_error:
            if self.debug:
                print(style(f"Error while connecting: {connection_error}", Style.RED), file=stderr)
            return None
        else:
            return self.client.recv(2048).decode()

    def send(self, data: Any, receive: bool=True) -> Any | None:
        """
        Send data to the host server.

        :param data: a string representing the data to send to the host
        :param return (default True): a boolean representing whether to wait for a reply
        :precondition: client must be initialized
        :postcondition: send data as bytes to the host and return the decoded reply
        :return: a string representing the reply from the host,
                 or None if an error occurred while connecting
        """
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as socket_error:
            if self.debug:
                print(style(f"Error while sending: {socket_error}", Style.RED), file=stderr)
            return None
        else:
            if receive:
                reply_in = pickle.loads(self.client.recv(2048))
                return reply_in
            return None


def main():
    client = Client()
    try:
        data = client.connect()
        message = ""
#        while message != "q" and data:
#            message = input("> ")
#            if not message:
#                continue
#            data = client.send(message)
#            if data is None:
#                print(style("Connection lost.", Style.RED))
#                break
#            print(data)
#            if data == "Starting game":
#                break

        # Have a 'send' here waiting for other player connection
        # start_game
        data = client.send("waiting...")
        while data != "start_game":
            print(data)
            if not data:
                return
            if data == "kick":
                client.send("acknowledged_kick", receive=False)
                return
            data = client.send("waiting")
        print("Starting Game...")

        while True:
            message = input("> ")
            if not message:
                continue
            data = client.send(message)
            if data is None:
                print(style("Connection lost.", Style.RED))
                return
            if data == "kick":
                break
            if not data["status"]:
                break
            print(data)
        print("Getting kicked...")
        while data != "kick":
            data = client.send("waiting")
            if not data:
                break
        client.send("acknowledged_kick", receive=False)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
