# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from work.protocol import Feeder


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
        self.assertEqual(
            (b'1', b''),
            self.feeder.feed(buffer)
        )

    def test_packet_partly(self):
        self.connection.recv.return_value = b'\x00'
        buffer = b''
        packet, buffer = self.feeder.feed(buffer)
        self.assertEqual(
            (None, b'\x00'),
            (packet, buffer)
        )
        self.connection.recv.return_value = b'\x00\x00\x01'
        packet, buffer = self.feeder.feed(buffer)
        self.assertEqual(
            (None, b''),
            (packet, buffer)
        )
        self.connection.recv.return_value = b'1'
        packet, buffer = self.feeder.feed(buffer)
        self.assertEqual(
            (b'1', b''),
            (packet, buffer)
        )

    def test_two_packets(self):
        self.connection.recv.return_value = b'\x00\x00\x00\x011\x00'
        buffer = b''
        packet, buffer = self.feeder.feed(buffer)
        self.assertEqual(
            (b'1', b'\x00'),
            (packet, buffer)
        )
        self.connection.recv.return_value = b'\x00\x00\x012'
        packet, buffer = self.feeder.feed(buffer)
        self.assertEqual(
            (b'2', b''),
            (packet, buffer)
        )

    def test_packet_with_data(self):
        self.connection.recv.return_value = b'\x00\x00\x00\x0C3hello world'
        buffer = b''
        packet, buffer = self.feeder.feed(buffer)
        self.assertEqual(
            (b'3hello world', b''),
            (packet, buffer)
        )
