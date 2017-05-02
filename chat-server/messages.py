#!usr/bin/env python3
"""
    Printing template large message
"""
import datetime


class Messages(object):
    """
        
        : commands
        info() :
        welcome_string() : 
        print_new_user() :
        client_list() :
        
    """

    def __init__(self, **kwargs):
        if kwargs['host'] is None:
            raise Exception('None value for "host" in "Messages"')
        elif kwargs['port'] is None:
            raise Exception('None value for "port" in "Messages"')
        elif kwargs['backlog'] is None:
            raise Exception('None value for "backlog" in "Messages"')
        else:
            self.server_info = kwargs

    def welcome_string(self):
        """ Server welcome string for admin """
        return "Running server on {} and" \
               "listening {} with listen {}".format(self.server_info['host'], self.server_info['port'],
                                                    self.server_info['backlog'])

    def print_new_user(self, login_string):
        """ New user on server """
        message = 'User "%s" connected to the room' % login_string
        head = 'Cchat~%s' % self.time()
        return {'head': head, 'message': message}

    def print_user_left(self, login_string):
        """ User left from chat"""
        message = 'User "%s" left from the room' % login_string
        head = 'Cchat~%s' % self.time()
        return {'head': head, 'message': message}

    @staticmethod
    def time():
        return str(datetime.datetime.now().time())[:16]
