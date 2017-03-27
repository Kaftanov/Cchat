#!/usr/bin/env python3
"""
    #############################
        Server application
        version python: python3
        based on socket
    #############################
"""
import socket
import sys
import select
import signal

import servermessage
from communication import send, receive


class Server:
    """
        object that are contained in the
            listen_count: max listening ports
            serv_host: location server in net
            serv_port: server's port
            command_list: special server command for user
                contain: ['/online', /info, ]
            command_string: string which contain command
            sid_value: session id value
            user_list: list of output client address
            user_dict: embedded dict which look like: {'sid_value': {
             'login': .., 'first_name': .., 'second_name': .., 'password': ..,
             'hostname':..},  ..}
        functions Server contain
            __init__
                info: initialize socket
                variable: listen_count, serv_host, serv_port
            sighandler
                info: shutting down server and closing all sockets
                variable: without variable
            serve
                info: main server's loop
                variable: without variable
            exec_commands
                info: execute commands from 'command_list'
                variable: command_string
    """
    def __init__(self, listen_count=None, serv_host=None, serv_port=None):
        if listen_count is None:
            listen_count = 5
        if serv_host is None:
            serv_host = 'localhost'
        if serv_port is None:
            serv_port = 3490

        self.server_password = 'qwerty'
        self.user_dict = {}
        self.user_list = []
        self.socket_sid_dict = {}
        # initialize server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((serv_host, serv_port))
        self.server.listen(listen_count)
        message = servermessage.welcome_string(serv_host, serv_port, listen_count)
        print(message)
        self.commands_list = ['/online',
                              '/info']
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """ Shutdown the server if typing Ctrl + C """
        # close all clients socket
        for sock in self.user_list:
            sock.close()
        # close main socket
        self.server.close()
        sys.exit('Shutting down server...')

    def exec_commands(self, command_string):
        """ Executing commands special commands """
        if command_string == '/online':
            return servermessage.client_list(self.user_dict)
        elif command_string == '/info':
            return servermessage.info()
        else:
            return 'Unexpected Error'

    def validation_user(self, data):
        """ Validating data which received from user"""
        if data['password'] == self.server_password:
            return True
        else:
            return False

    def broadcast_message(self, message):
        """ Broadcast messages for all users"""
        for sock in self.user_list:
            send(sock, message)

    def get_sid(self, sock):
        """ Getting sessionId_value """
        return self.socket_sid_dict[sock]

    def run_server_loop(self):
        input_socket_list = [self.server]
        is_running = True
        while is_running:
            try:
                in_fds, out_fds, err_fds = select.select(input_socket_list,
                                                         self.user_list, [])
            except select.error as error:
                print(error)
                break
            except socket.error as error:
                print(error)
                break

            for sock in in_fds:
                if sock is self.server:
                    user, user_address = self.server.accept()
                    # waiting data from client
                    # authentication form
                    data = receive(user)
                    # validator function
                    if self.validation_user(data):
                        sid_value = data['login'] + \
                                          chr(len(self.socket_sid_dict))
                        send(user, "Success")
                        self.user_dict[sid_value] = data
                        self.socket_sid_dict[user] = sid_value
                        print(self.user_dict[self.get_sid(user)])
                        message = 'Cchat@New User in room "%s"' % data['login']
                        # send message for all users
                        # broadcast function
                        self.broadcast_message(message)
                        # adding new client in output list
                        input_socket_list.append(user)
                        self.user_list.append(user)
                    else:
                        send(user, 'Error')
                        continue
                else:
                    try:
                        data = receive(sock)
                        if data:
                            if data in self.commands_list:
                                send(sock, self.exec_commands(data))
                            else:
                                message = self.user_dict[self.get_sid(sock)]['login'] + '@' + data
                                for i in self.user_list:
                                    if i is not sock:
                                        send(i, message)
                        else:
                            # message user left
                            message = 'Cchat@User left "%s"' % self.user_dict[self.get_sid(sock)]['login']
                            print(message)
                            sock.close()
                            input_socket_list.remove(sock)
                            self.user_list.remove(sock)
                            # message user
                            message = 'Cchat@Hung up "%s"' % self.user_dict[self.get_sid(sock)]['login']
                            self.broadcast_message(message)

                    except socket.error as error:
                        print(error)
                        input_socket_list.remove(sock)
                        self.user_list.remove(sock)
        self.server.close()


if __name__ == "__main__":
    Server().run_server_loop()
