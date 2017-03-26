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
        tuple_kwargs = ('first_name', 'second_name', 'password', 'hostname',
                        'login')
        # parse kwargs
        for key in tuple_kwargs:
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, 'Empty_field')


def create_userform():
    """ Creating initialization form for user"""
    print('...Login...')
    user_login = input('Login: ')
    first_name = input('First name: ')
    second_name = input('Second name: ')
    password = getpass('Please enter the password:')
    hostname = getuser()
    return UserForm(first_name=first_name, second_name=second_name,
                    password=password, hostname=hostname,
                    login=user_login).__dict__
