# coding=utf-8

from collections import OrderedDict

CONNECT = 0
PING = 1
PINGD = 2
QUIT = 3
QUITD = 4
FINISH = 5


class ProtocolMeta(type):

    registered_packets = {}

    def __init__(self, name, bases, dct):
        if dct.get('__abstract__'):
            return
        self.fields = OrderedDict()
        command_exists = False
        for key, value in dct.items():
            if isinstance(value, Command):
                assert value.command not in self.__class__.registered_packets, (
                    "Duplicate command!"
                )
                self.__class__.registered_packets[value.command] = self
                command_exists = True
            if isinstance(value, Field):
                value.name = key
                self.fields[key] = value
        assert command_exists, "Command should exists!"
        assert isinstance(list(self.fields.values())[0], Command), (
            "Command should be first argument"
        )

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()


class Field:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class String(Field):
    pass


class Integer(Field):
    pass


class Command(Field):

    def __init__(self, command):
        self.command = command


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
        return 'connected'


class Ping(Packet):
    command = Command(PING)

    def reply(self):
        return 'pong'


class PingD(Packet):
    command = Command(PINGD)
    data = String()

    def reply(self):
        return 'pongd ' + self.data


class Quit(Packet):
    command = Command(QUIT)

    def reply(self):
        return 'ackquit'


class QuitD(Packet):
    command = Command(QUITD)
    data = String()

    def reply(self):
        return 'ackquitd ' + self.data


class Finish(Packet):
    command = Command(FINISH)

    def reply(self):
        return 'ackfinish'


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
