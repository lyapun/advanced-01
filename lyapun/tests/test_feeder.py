# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from work.protocol import Feeder
from work.protocol.commands import Ping, PingD, PING, PINGD


class FeederTestCase(TestCase):

    def setUp(self):
        self.connection = Mock()
        self.feeder = Feeder(connection=self.connection)

    def test_empty_feed(self):
        self.connection.recv.return_value = b''
        buffer = b''
        self.assertEqual(
            (None, b''),
            self.feeder.feed(buffer)
        )

    def test_packet(self):
        self.connection.recv.return_value = b'\x00\x00\x00\x011'
        buffer = b''
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'', buffer)
        self.assertEqual(Ping, type(command))
        self.assertEqual(PING, command.command)

    def test_packet_partly(self):
        self.connection.recv.return_value = b'\x00'
        buffer = b''
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'\x00', buffer)
        self.assertEqual(None, command)

        self.connection.recv.return_value = b'\x00\x00\x01'
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'', buffer)
        self.assertEqual(None, command)

        self.connection.recv.return_value = b'1'
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'', buffer)
        self.assertEqual(Ping, type(command))
        self.assertEqual(PING, command.command)

    def test_two_packets(self):
        self.connection.recv.return_value = b'\x00\x00\x00\x011\x00'
        buffer = b''
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'\x00', buffer)
        self.assertEqual(Ping, type(command))
        self.assertEqual(PING, command.command)

        self.connection.recv.return_value = b'\x00\x00\x012'
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'', buffer)
        self.assertEqual(PingD, type(command))
        self.assertEqual(PINGD, command.command)

    def test_packet_with_data(self):
        self.connection.recv.return_value = b'\x00\x00\x00\x0C2hello world'
        buffer = b''
        command, buffer = self.feeder.feed(buffer)
        self.assertEqual(b'', buffer)
        self.assertEqual(PingD, type(command))
        self.assertEqual(PINGD, command.command)
        self.assertEqual('hello world', command.data)
