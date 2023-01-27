from socket import socket, AF_INET, SOCK_STREAM
from utils import *

def client():
    with socket(AF_INET, SOCK_STREAM) as client:
        try:
            client.connect(('127.0.0.1', 8820))
        except ConnectionRefusedError as e:
            print(f"{e}\nFirst run the server and then the client.")
            return
        command = ""
        while command != EXIT:
            command = input("Enter command: ").lower()
            if command == DIR or command == DELETE or command == EXE:
                command += f"{SEP}{input('Enter path: ')}"
            elif command == COPY:
                command += f"{SEP}{input('Enter file path: ')}"
                command += f"{SEP}{input('Enter new file path: ')}"
            send(client, command)
            print(f"{receive(client)}\n")

client()