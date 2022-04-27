"""
Created on Thu Apr  1 01:31:56 2021
"""

from typing import Union

import numpy as np

from errors.error_messages import AssumeX, AssumeXY
from errors.errors__the_number_line import EmptyList, NegativeValueFound


def check_list_len_2d(list_to_check):
    try:
        _list_to_check = list(list_to_check)
        if len(_list_to_check) == 0:
            raise EmptyList
        elif len(_list_to_check) == 1:
            AssumeX()
            _list_to_check.extend([0, 0])

        return _list_to_check
    except EmptyList:
        EmptyList(2)


def check_list_len_3d(list_to_check):
    try:
        _list_to_check = list(list_to_check)
        if len(_list_to_check) == 0:
            raise EmptyList
        elif len(_list_to_check) == 1:
            AssumeX()
            _list_to_check.extend([0, 0])
        elif len(_list_to_check) == 2:
            AssumeXY()
            _list_to_check.append(0)

        return _list_to_check
    except EmptyList:
        EmptyList(3)


def ensure_theta(theta: Union[list, float]):
    # in part taken from https://stackoverflow.com/a/50457453
    return [x % (2 * np.pi) for x in theta] if isinstance(theta, list) else theta % (2 * np.pi)


def ensure_phi(phi: Union[list, float]):
    # in part taken from https://stackoverflow.com/a/50457453
    return [x % np.pi for x in phi] if isinstance(phi, list) else phi % np.pi


def ensure_positive(args):
    _sum = np.sum(args, axis=0)
    if any(x < 0 for x in _sum):
        raise NegativeValueFound('Found negative sum, these parameters can not have a negative sum.')
