# coding=utf-8

import socket

from work.cmdargs import parse_arguments
from work import protocol


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1.0)
        self.host = host
        self.port = port

    def run_client(self):
        self.sock.connect((self.host, self.port))
        self.send_connect()
        self.enter_console()

    def close_client(self):
        self.sock.close()

    def send_connect(self):
        connect = protocol.Connect()
        self.sock.sendall(connect.pack())
        self.sock.recv(1024)

    def enter_console(self):
        print (
            "Hello! Just connected to server %(host)s:%(port)s" % dict(
                host=self.host,
                port=self.port,
            )
        )
        print (
            "Available commands:"
            "\n\t1 - Ping"
            "\n\t2 - Ping with data"
            "\n\t3 - Quit"
            "\n\t4 - Quit with data"
            "\n\t5 - Finish"
            "\nSelect one!"
        )
        while True:
            command_id = int(input('> '))
            data = ''
            if protocol.is_command_with_data(command_id):
                print("Enter data!")
                data = input('> ')
            command = protocol.construct_command_from_id(command_id, data)
            self.sock.sendall(command.pack())
            received_data = self.sock.recv(1024)
            print ("Recieved: ", received_data.decode('utf-8'))
            if command_id in [3, 4, 5]:
                break
        self.close_client()

if __name__ == '__main__':
    args = parse_arguments()
    client = Client(args.host, args.port)
    client.run_client()
