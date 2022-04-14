"""
Created on Wed Mar 24 18:44:02 2021
"""


class BaseErrorClass(Exception):
    pass


class FloatNotPassed(BaseErrorClass):
    pass


class MagnitudeIsLessThanZero(BaseErrorClass):
    pass


class DirectionIsNotPosNeg(BaseErrorClass):
    pass


class ListNotGiven(BaseErrorClass):
    pass


class ExtraParameterGiven(BaseErrorClass):
    pass


class EmptyList(BaseErrorClass):
    pass


class HmsIsNegative(BaseErrorClass):
    pass


class NegativeValueFound(BaseErrorClass):
    pass
