#!/usr/bin/env python3
"""
    Module for creating user_form_registration
        1. Personality
        2.
"""
from getpass import getpass, getuser


class UserForm:
    """
        Class: user_form_registration
    """
    def __init__(self, **kwargs):
        """
            Example input string:
                {'first_name': 'Ilya', 'second_name': 'Kaftanov',
                 'password' = 'password' 'hostname': 'getpass.getuser()'}

            tuple_kwargs -- tuple -- set of all args which you needed

        """
        tuple_kwargs = ('password',
                        'login')
        # parse kwargs
        for key in tuple_kwargs:
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, 'Empty_field')


def create_userform():
    """ Creating initialization form for user"""
    try:
        type_ = input('Are you already whith us? [Y/n]')
        if type_ in ('Yes', 'Y', 'yes', 'да', 'Да', 'y'):
            type_ = 'log'
        else:
            type_ = 'reg'
        if type_ == 'reg':
            print('...Registration...')
            login = input('Login: ')
            password = getpass('Password: ')
            if login and password:
                return 1, UserForm(password=password, login=login).__dict__
        elif type_ == 'log':
            print('...Login...')
            login = input('Login: ')
            password = getpass('Password: ')
            if login and password:
                return 0, UserForm(password=password, login=login).__dict__
    except KeyboardInterrupt as signal:
        print(signal, "Login form isn't correct")

