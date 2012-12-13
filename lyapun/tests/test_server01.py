# coding=utf-8

import signal
import socket
import subprocess
import logging
from unittest import TestCase
from time import sleep

from work.utils import prepare_data_for_sending, parse_recieved_bytes
from work.general import recieve_data_from_socket
from work.protocol.commands import (Connect, Ping, PingD, Quit, QuitD, Finish,
                                    Connected, Pong, PongD, AckQuit, AckQuitD,
                                    AckFinish)

logging.disable(logging.CRITICAL)


class ServerTestCase(TestCase):

    def setUp(self):
        self.server = subprocess.Popen(
            ['python', 'server01.py']
        )
        sleep(0.15)

    def tearDown(self):
        if self.server.poll() is None:
            self.server.send_signal(signal.SIGINT)
            self.server.wait()

    def _send_command(self, command):
        HOST = 'localhost'
        PORT = 50007
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.settimeout(1.0)
        sock.sendall(command)
        data = sock.recv(1024)
        sock.close()
        return data

    def test_connect(self):
        command = Connect()
        response = self._send_command(command.pack())
        self.assertEqual(Connected().pack(), response)

    def test_ping(self):
        command = Ping()
        response = self._send_command(command.pack())
        self.assertEqual(Pong().pack(), response)

    def test_pingd(self):
        data = 'hello world'
        command = PingD(data=data)
        response = self._send_command(command.pack())
        self.assertEqual(PongD(data=data).pack(), response)

    def test_quit(self):
        command = Quit()
        response = self._send_command(command.pack())
        self.assertEqual(AckQuit().pack(), response)

    def test_quitd(self):
        data = 'hello world'
        command = QuitD(data=data)
        response = self._send_command(command.pack())
        self.assertEqual(AckQuitD(data=data).pack(), response)

    def test_finish(self):
        command = Finish()
        response = self._send_command(command.pack())
        self.assertEqual(AckFinish().pack(), response)
        self.server.wait()
        self.assertEqual(0, self.server.poll())
