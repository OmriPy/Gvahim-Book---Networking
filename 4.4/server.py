from socket import socket, AF_INET, SOCK_STREAM
from typing import Dict
import os

root_dir = f'{os.getcwd()}{os.path.sep}webroot'

content_types: Dict[str, str] = {
    'txt': 'text/html; charset=utf-8',
    'html': 'text/html; charset=utf-8',
    'jpg': 'image/jpeg',
    'js': 'text/javascript; charset=UTF-8',
    'css': 'text/css'
}

unallowed_files = [f'{root_dir}{os.path.sep}unallowed.txt']

old_new_paths: Dict[str, str] = {
    f'{root_dir}{os.path.sep}imgs{os.path.sep}abstract.jpg': f'{os.path.sep}abstract.jpg'
}

def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()

def handle_client(client: socket):
    data = client.recv(1024).decode().split('\r\n')
    if not (data[0].startswith('GET /') and data[0].split(' ')[2] == 'HTTP/1.1'):
        print('status = 500')
        client.send('HTTP/1.1 500 Internal Server Error\r\n\r\n'.encode())
        return
    print('Valid packet')
    url_name = data[0].split(' ')[1]
    if url_name == '/':
        url_name += 'index.html'
    url_name = f"{root_dir}{url_name}"
    if os.path.isfile(url_name):
        if url_name in unallowed_files:
            status = 403
            bytes_packet = f'HTTP/1.1 {status} Forbidden\r\n\r\n'.encode()
        else:
            status = 200
            file_content = read_file(url_name)
            file_type = url_name.split(os.path.sep)[-1].split('.')[-1]
            print(f'{file_type = }')
            bytes_packet = f'HTTP/1.1 {status} OK\r\n'
            bytes_packet += f'Content-Length: {len(file_content)}\r\n'
            bytes_packet += f'Content-Type: {content_types.get(file_type)}\r\n\r\n'
            bytes_packet = bytes_packet.encode()
            bytes_packet += file_content
    elif url_name in old_new_paths.keys():
        status = 302
        bytes_packet = f'HTTP/1.1 {status} Moved Temporarily\r\n'.encode()
        bytes_packet += f'Location: {old_new_paths.get(url_name)}\r\n\r\n'.encode()
    else:
        status = 404
        bytes_packet = f'HTTP/1.1 {status} Not Found\r\n\r\n'.encode()
    print(f'{status = }')
    print('\n')
    client.send(bytes_packet)
    client.close()

def server():
    with socket(AF_INET, SOCK_STREAM) as server:
        try:
            server.bind(('0.0.0.0', 80))
        except OSError:
            print('Try again later')
            return
        print("Server is running\n")
        server.listen()
        while True:
            client, client_address = server.accept()
            print('Client connected')
            handle_client(client)


server()
