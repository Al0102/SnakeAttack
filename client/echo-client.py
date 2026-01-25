import socket

HOST_IP = "127.0.0.1"  # The host server's hostname/IP address
PORT = 65432  # The server's active port

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
