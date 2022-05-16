"""
Created on Thu Apr  1 01:31:56 2021
"""


class CartesianCoordinateSystemErorClass(Exception):
    pass


class ListNotGiven(CartesianCoordinateSystemErorClass):
    pass


class EmptyList(CartesianCoordinateSystemErorClass):
    pass


class AssumeX(CartesianCoordinateSystemErorClass):
    pass


class AssumeXY(CartesianCoordinateSystemErorClass):
    pass


def check_list_len_2d(list_to_check):
    _list_to_check = list(list_to_check)
    if len(_list_to_check) == 0:
        raise EmptyList('Empty list passed.')
    elif len(_list_to_check) == 1:
        AssumeX('Only one coordinate given, assuming the value to be x coordinate.')
        _list_to_check.extend([0, 0])

    return _list_to_check


def check_list_len_3d(list_to_check):
    _list_to_check = list(list_to_check)
    if len(_list_to_check) == 0:
        raise EmptyList('Empty list passed.')
    elif len(_list_to_check) == 1:
        AssumeX('Only one coordinate given, assuming the value to be x coordinate.')
        _list_to_check.extend([0, 0])
    elif len(_list_to_check) == 2:
        AssumeXY('Only two coordinates give, assuming the values to be x and y'
                 'coordinates.')
        _list_to_check.append(0)

    return _list_to_check
