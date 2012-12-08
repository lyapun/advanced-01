# coding=utf-8


def recieve_data_from_socket(connection):
    bytes = b''
    while len(bytes) < 2:
        bytes += connection.recv(1024)

    data_length_bytes = bytes[:2]
    data_length = int.from_bytes(data_length_bytes, byteorder='big')
    bytes = bytes[2:]

    while len(bytes) < data_length:
        bytes += connection.recv(1024)
    return bytes
