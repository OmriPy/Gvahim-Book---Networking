import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(('127.0.0.1', 8820))
    client.send("Omri".encode())
    message = client.recv(1024).decode()
    print(f"Got: {message}")