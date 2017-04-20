#!/usr/bin/env python3
"""
    #############################
        Server applycation
        version python: python3
        based on socket
    #############################
"""
import select
import socket
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QPoint

import userform
from cchatui import Ui_CchatWindow
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


class WorkThread(QThread):
    """
        Class for working with pyqt thread
        this class run 'run_chat_loop()' in class 'Client'
    """
    def __init__(self):
        QThread.__init__(self)

    def setWorker(self, Cl):
        self.Cl = Cl

    def run(self):
        self.Cl.run_chat_loop()


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
        self.prompt = '[%s $ ' % self.user_name
        self.initUI()

    def initUI(self):
        """ Initialize pyqt form"""
        application = QtWidgets.QApplication(sys.argv)
        CchatWindow = QtWidgets.QMainWindow()
        self.ui = Ui_CchatWindow()
        self.ui.setupUi(CchatWindow)
        self.ui.sendButton.clicked.connect(self.send_message)
        self.ui.inputLine.returnPressed.connect(self.send_message)
        CchatWindow.show()
        # set thread
        self.workThread = WorkThread()
        self.workThread.setWorker(self)
        self.workThread.start()
        sys.exit(application.exec_())

    def print_into_box(self, data):
        """ Printing data into text box"""
        self.ui.textBox.append(data)
        pass

    def send_message(self):
        """ Send message into socket"""
        # Warning error send message if unbound magic
        data = self.ui.inputLine.text()
        send_time = time.localtime(time.time())[3:6]
        time_string = '%s:%s:%s]' % (send_time[0],
                                     send_time[1],
                                     send_time[2])
        self.print_into_box(self.prompt + time_string + data)
        self.ui.inputLine.clear()
        send(self.sock, data)

    def validator_authenticate(self):
        """ Checking registration/login data"""
        is_authenticate = False
        while not is_authenticate:
            try:
                data = userform.create_userform()
                if data:
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
                else:
                    sys.exit('KeyboardInterrupt from user_form')
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
            in_fds, out_fds, err_fds = select.select([self.sock], [], [])
            for sock in in_fds:
                if sock is self.sock:
                    data = receive(self.sock)
                    if not data:
                        self.print_into_box('Server was shutdown')
                        is_shutdown = False
                        break
                    else:
                        data_list = data.split('@')
                        message = '<' + data_list[0] + '>' + data_list[1]
                        self.print_into_box(message)


if __name__ == "__main__":
    Client()
