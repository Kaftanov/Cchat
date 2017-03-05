import sys
import select
import socket
from communication import send, receive

BUFSIZ = 1024


class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host='localhost', port=3490):
        self.name = name
        # Quit flag
        self.flag = False
        self.port = port
        self.host = host
        # Initial prompt
        self.prompt = '['+'@'.join((name,
                                    socket.gethostname().split('.')[0]))+']> '
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print('Connected to chat server')
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error as error:
            print('Could not connect to chat server')
            print(error)
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
                            print('Shutting down.')
                            self.flag = True
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt as error:
                print ('Interrupted.', error)
                self.sock.close()
                break


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: %s name_id host portno' % sys.argv[0])
    client = ChatClient(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    client.cmdloop()
