#!usr/bin/env python3
"""
    Printing template large message
"""

class Messages(object):
    """
        
        : commands
        info() :
        welcome_string() : 
        print_new_user() :
        client_list() :
        
    """
    server_name = 'Cchat'
    promt = server_name + ':@'

    def __init__(self, **kwargs):
        if kwargs['host'] is None:
            raise Exception('None value for "host" in "Meessages"')
        elif kwargs['port'] is None:
            raise Exception('None value for "port" in "Messages"')
        elif kwargs['backlog'] is None:
            raise Exception('None value for "backlog" in "Messages"')
        else:
            self.server_info = kwargs

    def info(self):
        """ Some information about server """
        message = self.promt
        message += """
I'm Cchat and I'm glad to see you here :)
I have some commands special for you!
    /online - you can check who is online now
    /info
"""
        return message

    def welcome_string(self):
        """ Server welcome string for admin """
        return "Running server on {} and" \
               "listening {} with listen {}".format(self.server_info['host'],self.server_info['port'],
                                                    self.server_info['backlog'])

    def print_new_user(self, login_string):
        """ New user on server """
        return 'Cchat:@User "%s" connecting to the room' % login_string

    def client_list(self, user_dict):
        """ Print all online client """
        msg = 'Cchat:@'
        for i, key in enumerate(user_dict):
            msg += '#%i Client name: %s' % \
                   (i, user_dict[key]['login'])
        return msg




def full_client_list(user_dict):
    msg = 'Cchat:@'
    for i, key in enumerate(user_dict):
        msg += '#%i Login: "%s" \n First name: "%s"' \
               '\n Second name: "%s"' % (i,
                                         user_dict[key]['login'],
                                         user_dict[key]['first_name'],
                                         user_dict[key]['second_name'])
    return msg
