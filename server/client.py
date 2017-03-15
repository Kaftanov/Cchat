#!/usr/bin/env python3
"""
    #############################
        Server applycation
        version python: python3
        based on socket
    #############################
    # nothing to add
"""
import sys
import select
import socket
import userform
import pickle

from getpass import getpass, getuser
from communication import send, receive


class RegisterError(Exception):
    """
        My Exception
    """
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
                init socket, connect, getname form server
            cmdloop
                loop for wait writting message(send/receive)
    """
    def __init__(self, host='localhost', port=3490):
        """
            init client object
        """
        PORT = port
        HOST = host
        # Initial prompt
        self.prompt = '[unknown]> '
        log_flag = True
        while log_flag:
            try:
                pswd = getpass('Please enter the password:')
                print('Connected to chat server')
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((HOST, PORT))
                # check password
                send(self.sock, pswd)
                data = receive(self.sock)
                if data == 'Error':
                    raise RegisterError(0)
                elif data == 'Confirmed':
                    tmp = self.create_usrform()
                    send(self.sock, tmp)
                    self.prompt = '[' + tmp['name'] + ']> '
                    log_flag = False
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
                self.sock.close()
                sys.exit(1)

    def create_usrform(self):
        print('...Login...')
        name = input('Enter your name: ')
        long_name = input('Enter your full name: ')
        hostname = getuser()
        form = userform.UserForm(name=name, long_name=long_name,
                                 hostname=hostname)
        return form.__dict__

    def cmdloop(self):

        Q_flag = True
        while Q_flag:
            try:
                # !! if you notice that the form is always written
                # It's PROBLEM
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                # Wait for input from stdin & socket
                inputready, outputready, exceptrdy = select.select([0, self.sock], [], [])

                for i in inputready:
                    if i == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Shutting down.')
                            Q_flag = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt as error:
                print ('Interrupted.', error)
                self.sock.close()
                break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: %s name_id host portno' % sys.argv[0])

    Client(sys.argv[1], int(sys.argv[2])).cmdloop()
