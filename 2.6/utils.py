from socket import socket as __socket

__fill = 64

TIME = "time"
WHORU = "whoru"
RAND = "rand"
EXIT = "exit"

def __my_zfill(length: str) -> str:
    return '0' * (__fill - len(length)) + length

def receive(Socket: __socket) -> str:
    """Returns Socket.recv() appropriately."""
    bytes_length = int(Socket.recv(__fill).decode())
    return Socket.recv(bytes_length).decode()

def send(Socket: __socket, data: str):
    """Performs Socket.send(data) appropriately."""
    length = str(len(data.encode()))
    Socket.send(__my_zfill(length).encode())
    Socket.send(data.encode())