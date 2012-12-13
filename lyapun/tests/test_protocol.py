# coding=utf-8

from unittest import TestCase

from work.protocol.commands import (Connect, Packet, Ping, PingD, PING, PINGD,
                                CONNECT, Quit, Finish, FINISH, QuitD, QUITD,
                                QUIT)
from work.protocol.fields import Command, String
from work.protocol.meta import ProtocolMeta


class ProtocolTestCase(TestCase):

    def test_registered_packet(self):
        self.assertTrue(
            Ping in ProtocolMeta.registered_packets.values()
        )
        self.assertTrue(
            PingD in ProtocolMeta.registered_packets.values()
        )

    def test_register_packet_with_duplicate_command(self):
        with self.assertRaises(AssertionError):
            class DuplicatePing(Packet):
                command = Command(PING)

    def test_packet_without_command(self):
        with self.assertRaises(AssertionError):
            class NoCommand(Packet):
                data = String()

    def test_packet_with_bad_arg_order(self):
        with self.assertRaises(AssertionError):
            class BadOrder(Packet):
                data = String()
                command = Command(PING)


class ConnectTestCase(TestCase):

    def test_init(self):
        packet = Connect()
        self.assertEqual(
            CONNECT,
            packet.command
        )

    def test_pack(self):
        packet = Connect()
        self.assertEqual(b'\x00\x00\x00\x010', packet.pack())

    def test_unpack(self):
        packet = Packet.unpack(b'0')
        self.assertEqual(Connect, type(packet))
        self.assertEqual(CONNECT, packet.command)


class PingTestCase(TestCase):

    def test_init(self):
        ping = Ping()
        self.assertEqual(
            PING,
            ping.command
        )

    def test_pack(self):
        ping = Ping()
        self.assertEqual(b'\x00\x00\x00\x011', ping.pack())

    def test_unpack(self):
        packet = Packet.unpack(b'1')
        self.assertEqual(Ping, type(packet))
        self.assertEqual(PING, packet.command)


class PingDTestCase(TestCase):

    def test_init(self):
        pingd = PingD(data='hello world')
        self.assertEqual(PINGD, pingd.command)
        self.assertEqual('hello world', pingd.data)

    def test_pack(self):
        pingd = PingD(data='hello world')
        self.assertEqual(b'\x00\x00\x00\x0C2hello world', pingd.pack())

    def test_unpack(self):
        packet = Packet.unpack(b'2hello world')
        self.assertEqual(PingD, type(packet))
        self.assertEqual(PINGD, packet.command)
        self.assertEqual('hello world', packet.data)


class QuitTestCase(TestCase):

    def test_init(self):
        packet = Quit()
        self.assertEqual(
            QUIT,
            packet.command
        )

    def test_pack(self):
        packet = Quit()
        self.assertEqual(b'\x00\x00\x00\x013', packet.pack())

    def test_unpack(self):
        packet = Packet.unpack(b'3')
        self.assertEqual(Quit, type(packet))
        self.assertEqual(QUIT, packet.command)


class QuitDTestCase(TestCase):

    def test_init(self):
        packet = QuitD(data='hello world')
        self.assertEqual(QUITD, packet.command)
        self.assertEqual('hello world', packet.data)

    def test_pack(self):
        packet = QuitD(data='hello world')
        self.assertEqual(b'\x00\x00\x00\x0C4hello world', packet.pack())

    def test_unpack(self):
        packet = Packet.unpack(b'4hello world')
        self.assertEqual(QuitD, type(packet))
        self.assertEqual(QUITD, packet.command)
        self.assertEqual('hello world', packet.data)


class FinishTestCase(TestCase):

    def test_init(self):
        packet = Finish()
        self.assertEqual(
           FINISH,
            packet.command
        )

    def test_pack(self):
        packet = Finish()
        self.assertEqual(b'\x00\x00\x00\x015', packet.pack())

    def test_unpack(self):
        packet = Packet.unpack(b'5')
        self.assertEqual(Finish, type(packet))
        self.assertEqual(FINISH, packet.command)
