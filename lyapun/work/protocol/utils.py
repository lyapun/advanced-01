# coding=utf-8

from .commands import Packet, PINGD, QUITD


def is_command_with_data(command_id):
    assert isinstance(command_id, int)
    return command_id in [PINGD, QUITD]


def construct_command_from_id(command_id, data=''):
    assert isinstance(command_id, int)
    assert isinstance(data, str)
    bytes = (str(command_id) + data).encode('utf-8')
    return Packet.unpack(bytes)
