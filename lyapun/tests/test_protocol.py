# coding=utf-8

from unittest import TestCase

from work import protocol


class ProtocolTestCase(TestCase):

    def test_registered_packet(self):
        self.assertTrue(
            protocol.Ping in protocol.ProtocolMeta.registered_packets.values()
        )
        self.assertTrue(
            protocol.PingD in protocol.ProtocolMeta.registered_packets.values()
        )


class ConnectTestCase(TestCase):

    def test_init(self):
        packet = protocol.Connect()
        self.assertEqual(
            protocol.CONNECT,
            packet.command
        )

    def test_pack(self):
        packet = protocol.Connect()
        self.assertEqual(b'\x00\x00\x00\x010', packet.pack())

    def test_unpack(self):
        packet = protocol.Packet.unpack(b'0')
        self.assertEqual(protocol.Connect, type(packet))
        self.assertEqual(protocol.CONNECT, packet.command)


class PingTestCase(TestCase):

    def test_init(self):
        ping = protocol.Ping()
        self.assertEqual(
            protocol.PING,
            ping.command
        )

    def test_pack(self):
        ping = protocol.Ping()
        self.assertEqual(b'\x00\x00\x00\x011', ping.pack())

    def test_unpack(self):
        packet = protocol.Packet.unpack(b'1')
        self.assertEqual(protocol.Ping, type(packet))
        self.assertEqual(protocol.PING, packet.command)


class PingDTestCase(TestCase):

    def test_init(self):
        pingd = protocol.PingD(data='hello world')
        self.assertEqual(protocol.PINGD, pingd.command)
        self.assertEqual('hello world', pingd.data)

    def test_pack(self):
        pingd = protocol.PingD(data='hello world')
        self.assertEqual(b'\x00\x00\x00\x0C2hello world', pingd.pack())

    def test_unpack(self):
        packet = protocol.Packet.unpack(b'2hello world')
        self.assertEqual(protocol.PingD, type(packet))
        self.assertEqual(protocol.PINGD, packet.command)
        self.assertEqual('hello world', packet.data)


class QuitTestCase(TestCase):

    def test_init(self):
        packet = protocol.Quit()
        self.assertEqual(
            protocol.QUIT,
            packet.command
        )

    def test_pack(self):
        packet = protocol.Quit()
        self.assertEqual(b'\x00\x00\x00\x013', packet.pack())

    def test_unpack(self):
        packet = protocol.Packet.unpack(b'3')
        self.assertEqual(protocol.Quit, type(packet))
        self.assertEqual(protocol.QUIT, packet.command)


class QuitDTestCase(TestCase):

    def test_init(self):
        packet = protocol.QuitD(data='hello world')
        self.assertEqual(protocol.QUITD, packet.command)
        self.assertEqual('hello world', packet.data)

    def test_pack(self):
        packet = protocol.QuitD(data='hello world')
        self.assertEqual(b'\x00\x00\x00\x0C4hello world', packet.pack())

    def test_unpack(self):
        packet = protocol.Packet.unpack(b'4hello world')
        self.assertEqual(protocol.QuitD, type(packet))
        self.assertEqual(protocol.QUITD, packet.command)
        self.assertEqual('hello world', packet.data)


class FinishTestCase(TestCase):

    def test_init(self):
        packet = protocol.Finish()
        self.assertEqual(
            protocol.FINISH,
            packet.command
        )

    def test_pack(self):
        packet = protocol.Finish()
        self.assertEqual(b'\x00\x00\x00\x015', packet.pack())

    def test_unpack(self):
        packet = protocol.Packet.unpack(b'5')
        self.assertEqual(protocol.Finish, type(packet))
        self.assertEqual(protocol.FINISH, packet.command)
