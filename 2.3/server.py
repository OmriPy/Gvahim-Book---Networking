import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('0.0.0.0', 8820))
    print("Server connected")
    server.listen()
    while True:
        client, client_address = server.accept()
        message = client.recv(1024).decode()
        client.send(f"Hello {message}".encode())
        client.close()