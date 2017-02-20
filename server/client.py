import socket
import getpass


class ClientSocket(object):
    """
        Simple client socket class
    """
    def __init__(self, sock=None, host='localhost',
                 port=8080, data_size=1024):
        self.host = host
        self.port = port
        self.data_size = data_size
        if sock is None:
            self.clientsocket = socket.socket()
        else:
            self.clientsocket = sock

    def connection(self):
        """   """
        self.clientsocket.connect((self.host, self.port))
        send_message = 'Hello, I am %s. Nice to meat you' % (getpass.getuser())
        self.clientsocket.send(send_message.encode('ascii', 'ignore'))
        self.receive_message = b''
        tmp_data = self.clientsocket.recv(self.data_size)
        while tmp_data:
            self.receive_message += tmp_data
            tmp_data = self.clientsocket.recv(self.data_size)
        self.receive_message = self.receive_message.decode('utf-8')
        self.clientsocket.close()

    def print_answer(self):
        print(self.receive_message)


clientsocket = ClientSocket()
clientsocket.connection()
clientsocket.print_answer()
