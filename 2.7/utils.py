# __ = private
from socket import socket as __socket

SEP = '$'
DIR = 'dir'
DELETE = 'delete'
COPY = 'copy'
EXE = 'execute'
SCREENSHOT = 'screenshot'
SCREENSHOTS_PATH = r'/Users/omri/Documents/School/Python/30_12_2022/2.7/image.png'
EXIT = 'exit'

__fill = 64

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