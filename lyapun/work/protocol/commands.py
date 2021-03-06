# coding=utf-8

from .meta import ProtocolMeta
from .fields import Command, String

CONNECT = 0
PING = 1
PINGD = 2
QUIT = 3
QUITD = 4
FINISH = 5
CONNECTED = 6
PONG = 7
PONGD = 8
ACKQUIT = 9
ACKQUITD = 10
ACKFINISH = 11


class Packet(metaclass=ProtocolMeta):

    __abstract__ = True

    def __init__(self, **kwargs):
        keys = list(self.fields.keys())
        command = self.fields[keys[0]].command
        setattr(self, keys[0], command)
        for attr in keys[1:]:
            value = kwargs.get(attr)
            setattr(self, attr, value)

    def pack(self):
        bytes = b''
        for attr, value in self.fields.items():
            bytes += str(getattr(self, attr)).encode('utf-8')
        bytes_length = len(bytes)
        return bytes_length.to_bytes(4, byteorder='big') + bytes

    @classmethod
    def unpack(cls, data):
        assert isinstance(data, bytes)
        data = data.decode('utf-8')
        packet_cls = cls.__class__.registered_packets.get(int(data[0]))
        kwargs = {}
        for attr, attr_type in packet_cls.fields.items():
            if attr_type == Command:
                kwargs[attr] = data[0]
            else:
                kwargs[attr] = data[1:]
        return packet_cls(**kwargs)


class Connect(Packet):
    command = Command(CONNECT)

    def reply(self):
        return Connected().pack()


class Ping(Packet):
    command = Command(PING)

    def reply(self):
        return Pong().pack()


class PingD(Packet):
    command = Command(PINGD)
    data = String()

    def reply(self):
        return PongD(data=self.data).pack()


class Quit(Packet):
    command = Command(QUIT)

    def reply(self):
        return AckQuit().pack()


class QuitD(Packet):
    command = Command(QUITD)
    data = String()

    def reply(self):
        return AckQuitD(data=self.data).pack()


class Finish(Packet):
    command = Command(FINISH)

    def reply(self):
        return AckFinish().pack()


class Connected(Packet):
    command = Command(CONNECTED)


class Pong(Packet):
    command = Command(PONG)


class PongD(Packet):
    command = Command(PONGD)
    data = String()


class AckQuit(Packet):
    command = Command(ACKQUIT)


class AckQuitD(Packet):
    command = Command(ACKQUITD)
    data = String()


class AckFinish(Packet):
    command = Command(ACKFINISH)
