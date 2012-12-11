# coding=utf-8

import signal
import socket
import threading
import logging

from work.general import recieve_data_from_socket
from work.utils import prepare_data_for_sending
from work import protocol


class Server():

    do_stop = False

    def __init__(self, host, port):
        logging.info('Initialized server with host %s, port %d', host, port)
        self.orig_signal_handler = signal.signal(
            signal.SIGINT, self._kill_signal_handler
        )
        self.threads = []
        self.host = host
        self.port = port

    def run_server(self):
        self._initialize_socket(self.host, self.port)
        while not self.do_stop:
            try:
                conn, addr = self.sock.accept()
                logging.info("Accepted conn=%s, addr=%s", conn, addr)
                self._handle_client(conn, addr)
            except InterruptedError:
                pass
            except socket.timeout:
                pass
            except OSError as msg:
                logging.error("OSError: %s", msg)
                self.stop_server()
        self.stop_server()

    def stop_server(self):
        self.do_stop = True
        for thread in self.threads[:]:
            logging.info(
                "thread=%s, thread.is_alive=%s", thread, thread.is_alive()
            )
            thread.join()
        self.sock.close()
        logging.info("Socket closed, socket=%s", self.sock)
        signal.signal(signal.SIGINT, self.orig_signal_handler)

    def _initialize_socket(self, host, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.settimeout(1.0)
            self.sock.bind((host, port))
            self.sock.listen(5)
        except OSError as msg:
            logging.error("OSError: %s", msg)
            self.stop_server()

    def _handle_client(self, conn, addr):
        thread = threading.Thread(
            target=self._socket_handler, args=(conn, addr)
        )
        thread.start()
        self.threads.append(thread)

    def _socket_handler(self, conn, addr):
        conn.settimeout(1.0)
        while not self.do_stop:
            try:
                recieved_bytes = recieve_data_from_socket(conn)
                command = protocol.Packet.unpack(recieved_bytes)
                self._send_data_to_socket(conn, command.reply())
                if type(command) in [protocol.Quit, protocol.QuitD]:
                    conn.close()
                    break
                elif type(command) == protocol.Finish:
                    conn.close()
                    self.do_stop = True
                    break
            except socket.timeout:
                continue
            except OSError as msg:
                logging.error("OSError: %s", msg)
                self.stop_server()
        else:
            self._send_data_to_socket(conn, 'ackfinish')
            conn.close()

        self.threads.remove(threading.currentThread())
        logging.info("Thread off conn=%s", conn)

    def _send_data_to_socket(self, conn, data):
        try:
            conn.sendall(prepare_data_for_sending(data))
        except OSError as msg:
            logging.error("OSError: %s", msg)
            self.stop_server()

    def _kill_signal_handler(self, signum, frame):
        self.do_stop = True
        logging.info("Kill signal handler, do_stop=%s", self.do_stop)
