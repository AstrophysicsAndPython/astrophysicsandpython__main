#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 18:44:02 2021

@author: noonu
"""


class BaseErrorClass(Exception):
    pass


class IntNotPassed(BaseErrorClass):
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