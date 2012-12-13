# coding=utf-8

from collections import OrderedDict

from .fields import Command, Field


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
