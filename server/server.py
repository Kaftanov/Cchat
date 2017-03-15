#!/usr/bin/env python3
"""
    #############################
        Server applycation
        version python: python3
        based on socket
    #############################
    # nothing to add
"""
import socket
import sys
import select
import signal

from communication import send, receive
from large_message import info as get_information


class Server:
    """
        object that are contained in the
            clientmap -- dict -- {'client' : (client_adress, client_name)}
            outputs   -- list -- [all client sockets]
            backlog   -- int  -- max listening ports
            commands  -- list -- all spec commands
                contain: ['/online', /info, ]
        functions Server contain
            __init__
                initialize socket
            sighandler
                Shutting down server and closing all sockets
            getname
                get name,host from clientmap via inpust client
            serve
                main loop server
            exec_cmds
                execute commands from 'commands' for user
    """
    def __init__(self, backlog=5):
        HOST = 'localhost'
        PORT = 3490
        self.SERVERPSWD = 'qwerty'
        self.clientmap = {}
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(backlog)
        msg = "Running server on {HOST} and listening {PORT}".format(
                HOST=HOST, PORT=PORT)
        print(msg)
        self.commands = ['/online',
                         '/info']
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """
            Shutdown the server if typing Ctrl + C
        """
        # close all clients socket
        for item in self.outputs:
            item.close()
        # close main socket
        self.server.close()
        sys.exit('Shutting down server...')

    def getname(self, client):
        """
            Return the printable name of the
            client, given its socket...
        """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def exec_cmds(self, cmd):
        if cmd == '/online':
            msg = ''
            for i, item in enumerate(self.outputs):
                msg += '\n#%i Client name: %s::%s' % \
                       (i, self.clientmap[item][1], self.clientmap[item][2])
            return msg
        elif cmd == '/info':
            return get_information()
        else:
            return 'Unexpected Error'

    def serve(self):
        """
            main loop server
        """
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True

        while running:
            try:
                inputready, outputready, exceptready = select.select(
                                                      inputs, self.outputs, [])
            except select.error as error:
                print(error)
                break
            except socket.error as error:
                print(error)
                break
            for sock in inputready:
                if sock == self.server:
                    client, address = self.server.accept()
                    tmp_msg = "Cchat: got connection from {}".format(address)
                    print(tmp_msg)
                    # here server must get json or any variable
                    data = receive(client)

                    if data != 'qwerty':
                        send(client, 'Error')
                        continue
                    elif data == 'qwerty':
                        send(client, 'Confirmed')
                    else:
                        send(client, 'Unexpected Error')

                    data = receive(client)
                    client_name = data['name']
                    client_long_name = data['long_name']
                    inputs.append(client)
                    self.clientmap[client] = (address, client_name,
                                              client_long_name)
                    tmp_connect_msg = """\n(Connected: New client from
                    """.format(self.getname(client))
                    # send message for all users
                    for item in self.outputs:
                        send(item, tmp_connect_msg)
                    # add new client in outputs set
                    self.outputs.append(client)
                else:
                    try:
                        data = receive(sock)
                        if data:
                            if data in self.commands:
                                send(sock, self.exec_cmds(data))
                            else:
                                message = "\nUSER[{}]>> {}".format(
                                            self.getname(sock), data)

                                for item in self.outputs:
                                    if item is not sock:
                                        send(item, message)
                        else:
                            tmp_left_msg = "Cchat: {} left".format(
                                            {self.getname(client)})
                            print(tmp_left_msg)
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            msg = "\n(Hung up: Client from {})".format(
                                    {self.getname(sock)})
                            for item in self.outputs:
                                send(item, msg)

                    except socket.error as error:
                        print(error)
                        inputs.remove(sock)
                        self.outputs.remove(sock)
        self.server.close()


if __name__ == "__main__":
    Server().serve()
