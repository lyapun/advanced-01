# coding=utf-8

import signal
import socket
import subprocess
import logging
from unittest import TestCase
from time import sleep

from work.utils import prepare_data_for_sending, parse_recieved_bytes
from work.general import recieve_data_from_socket
from work import protocol

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
        data = recieve_data_from_socket(sock)
        sock.close()
        return data

    def test_connect(self):
        command = protocol.Connect()
        data = self._send_command(command.pack())
        self.assertEqual(b'connected', data)

    def test_ping(self):
        command = protocol.Ping()
        data = self._send_command(command.pack())
        self.assertEqual(b'pong', data)

    def test_pingd(self):
        command = protocol.PingD(data='hello world')
        data = self._send_command(command.pack())
        self.assertEqual(b'pongd\nhello\nworld', data)

    def test_quit(self):
        command = protocol.Quit()
        data = self._send_command(command.pack())
        self.assertEqual(b'ackquit', data)

    def test_quitd(self):
        command = protocol.QuitD(data='hello world')
        data = self._send_command(command.pack())
        self.assertEqual(b'ackquitd\nhello\nworld', data)

    def test_finish(self):
        command = protocol.Finish()
        data = self._send_command(command.pack())
        self.assertEqual(b'ackfinish', data)
        self.server.wait()
        self.assertEqual(0, self.server.poll())
