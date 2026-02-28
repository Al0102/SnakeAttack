from ansi_actions.style import Style, style

from sys import stderr

import socket


class Client:
    DEFAULT_HOST_IP = "127.0.0.1"
    DEFAULT_PORT = 63337

    def __init__(self, ip: str=DEFAULT_HOST_IP, port: int=DEFAULT_PORT):
        """
        Initialize a Client connection entity.

        :param ip: (default Client.DEFAULT_HOST_IP) a string representing the host IP address to connect to
        :param port: (default Client.DEFAULT_PORT) an integer representing the port of the connection
        """
        self.server_ip: str = ip
        self.port: int = port

        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr: Tuple[str, int] = (self.server_ip,  self.port)

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
            print(style(f"Error while connecting: {connection_error}", Style.RED), file=stderr)
            return None
        else:
            return self.client.recv(2048).decode()

    def send(self, data: str) -> str | None:
        """
        Send data to the host server.

        :param data: a string representing the data to send to the host
        :precondition: client must be initialized
        :postcondition: send data as bytes to the host and return the decoded reply
        :return: a string representing the reply from the host,
                 or None if an error occurred while connecting
        """
        try:
            self.client.send(str.encode(data))
        except socket.error as socket_error:
            print(style(f"Error while sending: {socket_error}", Style.RED), file=stderr)
            return None
        else:
            return self.client.recv(2048).decode("utf-8")


def main():
    client = Client()
    try:
        print(client.connect())
        message = ""
        data = True
        while message != "q" and data:
            message = input("> ")
            data = client.send(message)
            print(data)
    finally:
        client.client.close()


if __name__ == "__main__":
    main()
