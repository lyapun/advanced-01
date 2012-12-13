# coding=utf-8


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
