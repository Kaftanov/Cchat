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
import uuid
import datetime

from communication import send, receive
from messages import Messages
from dbworker import DbHandler
from cmdworker import Commands


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

        # set server messages worker
        self.MsgWorker = Messages(host=serv_host, port=serv_port, backlog=listen_count)
        # set data base worker
        self.DbWorker = DbHandler()
        # set command worker
        self.CmdWorker = Commands()

        self.uid_link = {}
        self.user_list = []
        self.server_password = 'qwerty'
        # initialize server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((serv_host, serv_port))
        self.server.listen(listen_count)

        print(self.MsgWorker.welcome_string())

        # set signal handler
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """ Shutdown the server if typing Ctrl + C """
        for sock in self.user_list:
            sock.close()
        self.server.close()
        sys.exit('Shutting down server...')

    def generate_uid(self, login):
        uid = self.DbWorker.get_uid_by_login(login)
        return uid if uid else str(uuid.uuid4())

    def authenticate_user(self, data):
        try:
            login = data['login']
            password = data['password']
            uid = self.generate_uid(login)

            if data['type'] == 'log':
                if password == self.DbWorker.get_passwd_by_login(login):
                    self.DbWorker.update_state(uid=uid, state=1, date='NULL')
                else:
                    return False,
            elif data['type'] == 'reg':
                user_form = {'uid': uid, 'login': login, 'password': password,
                             'state': 1, 'left': 'NULL'}
                self.DbWorker.add_user(user_form)
            else:
                return False,

            message = self.MsgWorker.print_new_user(login)

            return True, uid, message
        except KeyError as error:
            print(error)
            return False,

    def broadcast_message(self, message, sockt=None):
        """ Broadcast messages for all users"""
        if sockt is None:
            for sock in self.user_list:
                send(sock, message)
        else:
            for sock in self.user_list:
                if sock is not sockt:
                    send(sock, message)

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
                    data = receive(user)
                    request = self.authenticate_user(data)
                    if request[0]:
                        message = request[2]
                        self.broadcast_message(message)
                        self.uid_link[user] = request[1]
                        input_socket_list.append(user)
                        self.user_list.append(user)
                        send(user, 'Success')
                    else:
                        send(user, 'Error')
                        continue
                else:
                    try:
                        data = receive(sock)
                        if data:
                            print(data)
                            if data in self.CmdWorker.command_list:
                                send(sock, self.CmdWorker.execute_commands(data))
                            else:
                                user = self.DbWorker.get_user(self.uid_link[sock])['login']
                                head = '%s~%s' % (user, self.MsgWorker.time())
                                message = data
                                self.broadcast_message({'head': head, 'message': message}, sock)
                        else:
                            time = self.CmdWorker.time()
                            self.DbWorker.update_state(self.uid_link[sock], 0, time)
                            sock.close()
                            input_socket_list.remove(sock)
                            self.user_list.remove(sock)

                            message = self.MsgWorker.print_user_left(self.DbWorker.get_user(
                                self.uid_link[sock])['login'])
                            self.broadcast_message(message)

                    except socket.error as error:
                        print(error)
                        input_socket_list.remove(sock)
                        self.user_list.remove(sock)
        self.server.close()


if __name__ == "__main__":
    Server().run_server_loop()
