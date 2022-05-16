"""
Created on May 11 12:02:37 2022
"""


class BaseErrorClass(Exception):
    pass


class OutputTypeError(BaseErrorClass):
    pass


class IncompleteArguments(BaseErrorClass):
    pass
