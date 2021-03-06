# coding=utf-8

from .commands import Packet


class Feeder:

    def __init__(self, connection):
        self.connection = connection
        self.data_length = None

    def feed(self, buffer):
        buffer += self.connection.recv(1024)
        if not self.data_length:
            if len(buffer) >= 4:
                buffer = self._store_data_length(buffer)
        if self.data_length and len(buffer) >= self.data_length:
            return self._get_command_and_buffer(buffer)
        else:
            return None, buffer

    def _store_data_length(self, buffer):
        data_length_bytes = buffer[:4]
        buffer = buffer[4:]
        self.data_length = int.from_bytes(
            data_length_bytes, byteorder='big'
        )
        return buffer

    def _get_command_and_buffer(self, buffer):
        packet = buffer[:self.data_length]
        command = Packet.unpack(packet)
        buffer = buffer[self.data_length:]
        self.data_length = None
        return command, buffer
