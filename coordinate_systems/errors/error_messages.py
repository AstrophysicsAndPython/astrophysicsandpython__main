"""
Created on Wed Mar 24 18:46:09 2021
"""


def FloatNotPassed():
    print('Parameter type should be int.')


def MagnitudeIsLessThanZero():
    print('Magnitude cannot be less than 0.')


def DirectionIsNotPosNeg():
    print('Direction can either be positive or negative only.')


def ListNotGiven():
    print('The input required is a list.')


def ExtraParameterGiven(req=None, given=None):
    if given is None:
        print(f'Only {req} parameters are required.')
    else:
        print(f'{given} parameters given in list, only {req} are required.')


def EmptyList(num=None):
    print(f'Empty list passed. A list of {num} is required.')


def AssumeX():
    print('Only one coordinate given, assuming the value to be x coordinate.')


def AssumeXY():
    print('Only two coordinates give, assuming the values to be x and y coordinates.')


def HmsIsNegative():
    print('HMS cannot be negative.')


def NegativeValueFound():
    print(f'Raised NegativeValueFound error: Found negative sum, these parameters can'
          f'not have a negative sum.')
