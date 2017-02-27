<<<<<<< HEAD
import select
import socket
import sys
import signal
from communication import send, receive

BUFSIZ = 1024


class ChatServer(object):
    """
        Simple chat server using select
    """

    def __init__(self, port=3490, backlog=5):
        self.clients = 0
        # Client map
        self.clientmap = {}
        # Output socket list
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', port))
        print 'Listening to port', port, '...'
        self.server.listen(backlog)
        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """
            Shutdown the server if typing Ctrl+C
        """
        # Close the server
        print 'Shutting down server...'
        # Close existing client sockets
        for sock in self.outputs:
            sock.close()
        # Closing the server port
        self.server.close()

    def getname(self, client):
        """
            Return the printable name of the
            client, given its socket...
        """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def serve(self):
        """

        """
        inputs = [self.server, sys.stdin]
        self.outputs = []

        running = 1

        while running:

            try:
                inputready, outputready, exceptready = select.select(
                                                      inputs, self.outputs, [])
            except select.error as error:
                break
            except socket.error as error:
                break

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print 'chatserver: got connection %d from %s' % (
                                                      client.fileno(), address)
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)

                    self.clientmap[client] = (address, cname)
                    # Send joining information to other clients
                    msg = '\n(Connected: New client (%d) from %s)' % (
                                            self.clients, self.getname(client))
                    for o in self.outputs:
                        # o.send(msg)
                        send(o, msg)

                    self.outputs.append(client)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    # handle all other sockets
                    try:
                        # data = s.recv(BUFSIZ)
                        data = receive(s)
                        if data:
                            # Send as new client's message...
                            msg = '\n#[' + self.getname(s) + ']>> ' + data
                            # Send data to all except ourselves
                            for o in self.outputs:
                                if o != s:
                                    # o.send(msg)
                                    send(o, msg)
                        else:
                            print 'chatserver: %d hung up' % s.fileno()
                            print 'chatserver: %s left room' % (
                                   self.getname(client))
                            self.clients -= 1
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                            # Send client leaving information to others
                            msg = '\n(Hung up: Client from %s)' % self.getname(s)
                            for o in self.outputs:
                                # o.send(msg)
                                send(o, msg)

                    except socket.error as error:
                        # Remove
                        inputs.remove(s)
                        self.outputs.remove(s)
        self.server.close()


if __name__ == "__main__":
    ChatServer().serve()
=======
import socket
import sys


class ServerSocket(object):
    """
        Class includes all of the method work server
    """
    def __init__(self, sock=None, host='', port=8080, listen_count=1,
                 data_size=1024):
        """Init socket"""
        if sock is None:
            self.serversocket = socket.socket()
        else:
            self.serversocket = sock

        self.serversocket.bind((host, port))
        self.serversocket.listen(listen_count)
        self.host = host
        self.port = port
        self.listen_count = listen_count
        self.data_size = data_size

    def getinfo(self):
        print('Information about object:',
              """serversocket=%s
                 host=%s
                 port=%s
                 listen_count=%s
                 data_size=%s
              """ % (self.serversocket, self.host, self.port,
                     self.listen_count, self.data_size))

    def checkErrors(self):
        """Function for checking args of Class
           If found empty args return error and exit
        """
        try:
            self.host
            self.port
            self.listen_count
            self.data_size
            self.serversocket
        except AttributeError as error:
            print('Error in atribute for socket', error)
            sys.exit(1)
        else:
            print('All args are well :)')

    def start_server(self):
        """Start server function"""
        # check error whith help spec function
        self.checkErrors()
        try:
            while True:
                print('Wait clientsocket...')
                (clientsocket, address) = self.serversocket.accept()
                try:
                    print('New connection from ' + address[0])
                    clientsocket.settimeout(60)
                    data = clientsocket.recv(self.data_size)

                    if not data:
                        print('timeout error: "No Data"')
                        clientsocket.close()

                    self.receive_message = data.decode('utf-8')
                    print(self.receive_message)
                    send_message = 'Hello you are %s' % (address[0])
                    clientsocket.send(send_message.encode('ascii', 'ignore'))
                except socket.error:
                    print('Socket error')
                    clientsocket.close()
                    sys.exit(1)
                finally:
                    clientsocket.close()
        except KeyboardInterrupt:
            print('--->EXIT')
            sys.exit(1)
        finally:
            self.serversocket.close()


serversocket = ServerSocket(listen_count=1, data_size=16384)
serversocket.start_server()
# serversocket.getinfo()
>>>>>>> master
