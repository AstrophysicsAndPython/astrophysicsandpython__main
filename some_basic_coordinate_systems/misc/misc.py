"""
Created on Thu Apr  1 01:31:56 2021
"""

from ..errors.error_base import EmptyList
from ..errors.error_messages import AssumeX, AssumeXY


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
