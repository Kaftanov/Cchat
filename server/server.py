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
