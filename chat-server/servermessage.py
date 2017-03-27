#!usr/bin/env python3
"""
    Printing template large message
"""


def info():
    message = """
    I'm Cchat and I'm glad to see you here :)
    I have some commands special for you!
        /online - you can check who is online now
        / ...
    """
    return message


def welcome_string(host='localhost', port=3490, backlog=5):
    return "Running server on {} and" \
           "listening {} with listen {}".format(host, port, backlog)


def client_list(output_list):
    msg = ''
    for i, arg in enumerate(output_list):
        msg += '\n#%i Client name: %s' % \
              (i, output_list[arg]['login'])
    return msg
