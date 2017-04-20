#!/usr/bin/env python3
"""
    #############################
        Server application || TCP, socket
        version python: python3
    #############################
"""
import select
import signal
import socket
import sys

from communication import send, receive
from messages import Messages
from dbworker import DbHandler

class Server:
    """
        object that are contained in the
            listen_count: max listening ports
            serv_host: location server in net
            serv_port: server's port
            command_list: special server command for user
                contain: ['/online', /info, ]
            command_string: string which contain command
            user_list: list of output client address
            user_dict: embedded dict which look like: {'sid_value': {
             'login': .., 'first_name': .., 'second_name': .., 'password': ..,
             'hostname':..},  ..}
            socket_sid_dict: contain session id value (sid_value) and linking with socket
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
            validation_user
                info: checking if user's password is valid
                variable: dict with key ['password']
            broadcast_message
                info: sending message on all socket, which contain in self.user_list
                 variable: string text
            get_sid
                info: get session id from socket dict
                variable: socket 
    """
    def __init__(self, listen_count=None, serv_host=None, serv_port=None):
        if listen_count is None:
            listen_count = 5
        if serv_host is None:
            serv_host = 'localhost'
        if serv_port is None:
            serv_port = 3490

        # set server messages
        self.Message = Messages(host=serv_host, port=serv_port, backlog=listen_count)
        # set data base worker
        self.DBHandler = DbHandler()

        self.server_password = 'qwerty'
        self.user_dict = {}
        self.user_list = []
        self.socket_sid_dict = {}
        # initialize server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((serv_host, serv_port))
        self.server.listen(listen_count)

        print(self.Message.welcome_string())

        self.commands_list = ['/online',
                              '/info']
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """ Shutdown the server if typing Ctrl + C """
        for sock in self.user_list:
            sock.close()
        self.server.close()
        sys.exit('Shutting down server...')

    def exec_commands(self, command_string):
        """ Executing special server commands """
        if command_string == '/online':
            return self.Message.client_list(self.user_dict)
        elif command_string == '/info':
            return self.Message.info()
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
                        # Need update this request
                        send(user, "Success")
                        self.user_dict[sid_value] = data
                        self.socket_sid_dict[user] = sid_value
                        # address : concat getpeername[0] + ' ' + getpeername[1]
                        message = self.Message.print_new_user(data['login'])
                        # send message for all users
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
                            try:
                                remote_dict = self.user_dict.pop(self.get_sid(sock))
                                remote_user = remote_dict['login']
                            except KeyError as error:
                                print(error)
                                remote_user = 'UNKNOWN'
                                pass

                            message = 'User "%s" left' % remote_user
                            print(message)
                            sock.close()
                            input_socket_list.remove(sock)
                            self.user_list.remove(sock)
                            # message user
                            message = 'Cchat@User "%s" left' % remote_user
                            self.broadcast_message(message)

                    except socket.error as error:
                        print(error)
                        input_socket_list.remove(sock)
                        self.user_list.remove(sock)
        self.server.close()


if __name__ == "__main__":
    Server().run_server_loop()
