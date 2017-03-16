#!/usr/bin/env python3
"""
    Module for creating user_form_registration
        1. Personality
        2.
"""


class UserForm:
    """
        Class: user_form_registration
    """
    def __init__(self, **kwargs):
        """
            Example input string:
                {'name': 'Ilya', 'long_name': 'Kaftanov Ilya Andreevich',
                 'hostname': 'getpass.getuser()'}

            tuple_kwargs -- tuple -- set of all args which you needed

        """
        tuple_kwargs = ('name', 'long_name', 'hostname')
        # parce kwargs
        for key in tuple_kwargs:
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, 'Empty_field')
