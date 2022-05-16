"""
Created on Wed Mar 24 18:44:02 2021
"""


class NumberLineErrorClass(Exception):
    pass


class FloatNotPassed(NumberLineErrorClass):
    pass


class MagnitudeIsLessThanZero(NumberLineErrorClass):
    pass


class DirectionIsNotPosNeg(NumberLineErrorClass):
    pass
