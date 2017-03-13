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
import getpass
import json
from communication import send, receive


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

    def __init__(self, host='localhost', port=3490,
                 usr_form=userform.UserForm()):
        """
            init client object
        """
        # User form it's all inf about auth user
        user_object_dict = usr_form.__dict__
        self.name = user_object_dict['name']
        self.user_object_json = json.dumps(user_object_dict)
        # Client object's
        PORT = port
        HOST = host
        # Initial prompt
        self.prompt = '['+'@'.join((name,
                                    socket.gethostname().split('.')[0]))+']> '
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            print('Connected to chat server')
            # Send information about user (user_object_json)
            send(self.sock, self.user_object_json)
            data = receive(self.sock)
            # Contains client address, set it
            # CLIENT split iter for identif user
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error as error:
            print('Cchat_Client: Could not connect to chat server')
            print(error)
            sys.exit(1)

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
    # login in chatroom
    print('...Login...')
    name = input('Enter your name: ')
    long_name = input('Enter your full name: ')
    hostname = getpass.getuser()
    form = userform.UserForm(name=name, long_name=long_name, hostname=hostname)

    Client(sys.argv[1], int(sys.argv[2]), form).cmdloop()
