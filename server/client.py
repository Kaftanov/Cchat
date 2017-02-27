import socket
<<<<<<< HEAD
import sys
import select
from communication import send, receive

BUFSIZ = 1024


class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host='127.0.0.1', port=3490):
        self.name = name
        # Quit flag
        self.flag = False
        self.port = int(port)
        self.host = host
        # Initial prompt
        self.prompt = '['+'@'.join((name,
                                    socket.gethostname().split('.')[0]))+']> '
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print 'Connected to chat server@%d' % self.port
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error as error:
            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def cmdloop(self):

        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin & socket
                inputready, outputready, exceptrdy = select.select([0, self.sock], [],[])

                for i in inputready:
                    if i == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print 'Shutting down.'
                            self.flag = True
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print 'Interrupted.'
                self.sock.close()
                break


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: %s chatid host portno' % sys.argv[0])

    client = ChatClient(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    client.cmdloop()
=======
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
>>>>>>> master
