#!/usr/bin/env python3
"""
    #############################
        Server applycation
        version python: python3
        based on socket
    #############################
"""
import sys
import select
import socket

import userform
from communication import send, receive



class RegisterError(Exception):
    """ My exception for user's password """
    def __init__(self, type_exception):
        Exception.__init__(self)
        if type_exception == 0:
            self.msg = "Cchat_Client: You password isn't correct, sry"
        elif type_exception == 1:
            self.msg = "Unexpected exception"

    def __str__(self):
        return self.msg


class Client:
    """
        Client is contain
            prompt -- string -- it's need for visual effect command line
        functions Server contain
            __init__
                init socket, connect, get name form server
            cmdloop
                loop for wait witting message(send/receive)
    """
    def __init__(self, server_host=None, server_port=None):
        """ init client object """
        if server_host is None:
            self.server_host = 'localhost'
        else:
            self.server_host = server_host
        if server_port is None:
            self.server_port = 3490
        else:
            self.server_port = server_port
        # Initial prompt
        self.user_name = self.validator_authenticate()
        self.prompt = '[%s]' % self.user_name

    def validator_authenticate(self):
        """ Checking registration/login data"""
        is_authenticate = False
        while not is_authenticate:
            try:
                data = userform.create_userform()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.server_host, self.server_port))
                send(self.sock, data)
                receive_data = receive(self.sock)
                # checking is user available
                if receive_data == 'Error':
                    raise RegisterError(0)
                elif receive_data == 'Success':
                    is_authenticate = True
                    return data['login']
                else:
                    raise RegisterError(1)

            except socket.error as error:
                print('Cchat_Client: Could not connect to chat server')
                print(error)
                sys.exit(1)

            except RegisterError as msg:
                print(msg)
                print("Try again")
                self.sock.close()

            except KeyboardInterrupt as signal:
                print(signal)
                if self.sock:
                    self.sock.close()
                sys.exit(1)

    def run_chat_loop(self):
        is_shutdown = True
        while is_shutdown:
            try:
                # !! if you notice that the form is always written
                # It's PROBLEM
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                in_fds, out_fds, err_fds = select.select([0, self.sock], [], [])

                for i in in_fds:
                    if i is 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif i is self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Shutting down.')
                            is_shutdown = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt as error:
                print ('Interrupted.', error)
                self.sock.close()
                break


if __name__ == "__main__":
    #if len(sys.argv) < 2:
        #sys.exit('Usage: %s name_id host portno' % sys.argv[0])
    Client().run_chat_loop()
