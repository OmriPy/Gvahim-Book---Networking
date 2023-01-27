from socket import socket, AF_INET, SOCK_STREAM
from utils import *
from glob import glob
from os import system
from os.path import join
from sys import platform
from shutil import copy
from subprocess import call
from pyautogui import screenshot
from typing import Callable, Dict

def dir():
    dir_path = join(recv_args[1], r'**')
    files = glob(dir_path)
    send(client, '\n'.join(files))

def delete():
    command = ""
    if platform == "darwin" or platform == "linux":
        command = "rm"
    elif platform == "win32":
        command = "rd"
    else: return
    try:
        system(f'{command} -r {recv_args[1]}')
    except Exception as e:
        send(client, f"Deletion went wrong!\n{e}")
        return
    send(client, "Deletion Succeeded!")

def copy_file():
    try:
        copy(recv_args[1], recv_args[2])
    except Exception as e:
        send(client, f"Copying went wrong!\n{e}")
        return
    send(client, "Copying Succeeded!")

def execute():
    try:
        if platform == 'win32' or platform == 'linux':
            retcode = call([recv_args[1]])
        elif platform == 'darwin':
            retcode = call(['open', recv_args[1]])
    except Exception as e:
        send(client, f"Execution went wrong!\n{e}")
        return
    print(f"{padding}Program returned with exit code: {retcode}")
    if retcode != 0:
        send(client, "Execution went wrong!")
        return
    send(client, "Execution Succeeded!")

def take_screenshot():
    try:
        img = screenshot()
        img.save(SCREENSHOTS_PATH)
    except Exception as e:
        send(client, f'Taking screenshot went wrong!\n{e}')
        return
    send(client, 'Screenshot was took successfully!')

def terminate():
    send(client, "Client closing")
    client.close()

COMMANDS: Dict[str, Callable[[None], None]] = {
    DIR: dir,
    DELETE: delete,
    COPY: copy_file,
    EXE: execute,
    SCREENSHOT: take_screenshot,
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
        print("Client connected\n\nCommands:")
        cmd_num = 1
        inc_cmd_num = None
        while True:
            global padding
            padding = ' ' * len(f'{cmd_num}. ')
            global recv, recv_args
            recv = receive(client)
            recv_args = recv.split(SEP)
            if recv_args[0] in [DIR, DELETE, EXE]:
                print(f"{cmd_num}. {recv_args[0]} {recv_args[1]}")
                inc_cmd_num = True
            elif recv_args[0] == COPY:
                print(f"{cmd_num}. {COPY} {recv_args[1]}\n{padding} ->  {recv_args[2]}")
                inc_cmd_num = True
            elif recv == SCREENSHOT or recv == EXIT:
                print(f"{cmd_num}. {recv}")
                inc_cmd_num = True
            else:
                inc_cmd_num = False

            if recv_args[0] in COMMANDS.keys():
                COMMANDS.get(recv_args[0])()
                if recv_args[0] == EXIT:
                    return
            else:
                send(client, "Command not found")
            if inc_cmd_num:
                cmd_num += 1

server()