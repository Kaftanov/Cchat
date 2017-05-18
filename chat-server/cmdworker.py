"""
    Command worker
"""
from dbworker import DbHandler
import datetime

class Commands(object):
    """
    
    """

    def __init__(self):
        """ """
        self.promt = '<<$$>>'

        self.DBHandler = DbHandler()

        self.command_list = ['/online',
                             '/info']

    def execute_commands(self, command):
        """ Executing user's commnds for server"""
        if command in self.command_list:
            if command == '/online':
                return self.online()
            elif command == '/info':
                return self.info()

    def online(self):
        """  """
        users = self.DBHandler.get_online_users()
        head = 'Cchat~%s' % self.time()
        if len(users) > 1:
            message = ''
            for user in users:
                message += user['login'] + '\n'

            return {'head': head, 'message': message}
        else:
            return {'head': head, 'message': 'No one is online. You are alone.'}

    def info(self):
        """ """
        head = 'Cchat~%s' % self.time()
        message = """
I'm Cchat and I'm glad to see you here :)
I have some commands special for you!
    /online - you can check who is online now
    /info"""
        return {'head': head, 'message': message}

    def cmd_list(self):
        return self.command_list

    @staticmethod
    def time():
        return str(datetime.datetime.now().time())[:16]