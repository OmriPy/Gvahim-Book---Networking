ID_LOCATION = 12

def find_web_address(data: bytes) -> bytes:
    data = data[ID_LOCATION:]
    return data[:data.index(b'\x00')]
