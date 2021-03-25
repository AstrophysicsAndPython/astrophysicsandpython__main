#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 18:46:09 2021

@author: noonu
"""


def IntNotPassed():
    print('Parameter type should be int.')


def MagnitudeIsLessThanZero():
    print('Magnitude cannot be less than 0.')


def DirectionIsNotPosNeg():
    print('Direction can either be positive or negative only.')


def ListNotGiven():
    print('The input required is a list.')


def ExtraParameterGiven(req=None, given=None):
    print('{} parameters given in list, only {} are required.'.format(req, given))


def EmptyList(num=None):
    print('Empty list passed. A list of {} inputs is required.'.format(num))


def AssumeX():
    print('Only one coordinate given, assuming the value to be movement in x coordinates.\n')


def AssumeXY():
    print('Only two coordinates give, assuming the values to be movement in x and y coordinates.\n')
