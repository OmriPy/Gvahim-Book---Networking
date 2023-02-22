from socket import socket, AF_INET, SOCK_STREAM
import os

def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()

def handle_client(client: socket):
    data = client.recv(1024).decode().split('\r\n')
    if not (data[0].startswith('GET /') and data[0].split(' ')[2] == 'HTTP/1.1'):
        client.close()
        return
    print('Valid packet\n')
    url_name = data[0].split(' ')[1]
    if url_name == '/':
        url_name += 'index.html'
    url_name = f"{os.getcwd()}{os.path.sep}webroot{url_name}"
    if not os.path.isfile(url_name):
        client.close()
        return
    client.send('HTTP/1.1 200 OK\r\n\r\n'.encode() + read_file(url_name))
    client.close()

def server():
    with socket(AF_INET, SOCK_STREAM) as server:
        try:
            server.bind(('0.0.0.0', 80))
        except OSError as e:
            print('Try again later')
            return
        print("Server is running")
        server.listen()
        while True:
            client, client_address = server.accept()
            print('Client connected')
            handle_client(client)


server()
