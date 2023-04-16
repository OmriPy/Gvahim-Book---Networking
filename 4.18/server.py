from socket import socket, AF_INET, SOCK_DGRAM
from utils import find_web_address

DNS_SERVER_IP = '0.0.0.0'
DNS_SERVER_PORT = 53
DEFUALT_BUFFER_SIZE = 1024
DESTINATION_IP = b'\xD4\x8F\x46\x28'


def response_query(data: bytes) -> bytes:
    id = data[:2]
    flags = b'\x81\x80'
    questions = data[4:6]
    answer = b'\x00\x01'
    authority = b'\x00\x00'
    additional = b'\x00\x00'
    queries = data[12:]
    name = b'\xc0\x10'
    response_type = b'\x00\x01' # type A
    response_class = b'\x00\x01'
    time_to_live = b'\x00\x00\x00\x3c' # 60 seconds
    data_length = b'\x00\x04' # ipv4 has 4 bytes
    return id + flags + questions + answer + authority + additional + queries + name + response_type\
            + response_class + time_to_live + data_length + DESTINATION_IP

def dns_handler(server_socket: socket, data: bytes, address: tuple):
    web_address = find_web_address(data)
    if web_address == b'\x03www\x06google\x02co\x02il':
        print('Got www.google.co.il DNS request query, sending response query')
        server_socket.sendto(response_query(data), address)

def server(ip: str, port: int):
    with socket(AF_INET, SOCK_DGRAM) as server:
        try:
            server.bind((ip, port))
        except OSError:
            print('Try again later')
            return
        print('DNS Server Connected')
        while True:
            try:
                data, address = server.recvfrom(DEFUALT_BUFFER_SIZE)
                dns_handler(server, data, address)
            except Exception as e:
                print(f'Client Exception\n{e}')


server(DNS_SERVER_IP, DNS_SERVER_PORT)
