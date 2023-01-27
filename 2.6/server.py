from socket import socket, AF_INET, SOCK_STREAM
from utils import *
from time import strftime
from random import randint
from typing import Dict, Callable

def time():
    send(client, strftime("%A, %d %B %Y"))

def whoru():
    send(client, "Omri's server")

def rand():
    send(client, str(randint(1, 10)))

def terminate():
    send(client, "Client closing")
    client.close()

COMMANDS: Dict[str, Callable[[None], None]] = {
    TIME: time,
    WHORU: whoru,
    RAND: rand,
    EXIT: terminate
}

def server():
    with socket(AF_INET, SOCK_STREAM) as server:
        try:
            server.bind(('0.0.0.0', 8820))
        except OSError as e:
            print(f"{e}\nTry again later.")
            return
        print("Server is running")    
        server.listen()
        global client
        client, client_address = server.accept()
        print("Client connected")
        while True:
            message_recv = receive(client)
            print(message_recv)
            if message_recv in COMMANDS.keys():
                COMMANDS.get(message_recv)()
                if message_recv == EXIT:
                    return
            else:
                send(client, "Command not found")

server()