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
        while command != "exit":
            command = input("Enter command: ").lower()
            send(client, command)
            print(f"{receive(client)}\n")

client()