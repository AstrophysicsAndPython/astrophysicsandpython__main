#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 01:31:56 2021

@author: noonu
"""

import errors.error_base as eb
import errors.error_messages as em


def check_list_len_2d(list_to_check):
    try:
        _list_to_check = list(list_to_check)
        if len(_list_to_check) == 0:
            raise eb.EmptyList
        elif len(_list_to_check) == 1:
            em.AssumeX()
            _list_to_check.extend([0, 0])

        return _list_to_check
    except eb.EmptyList:
        em.EmptyList(2)


def check_list_len_3d(list_to_check):
    try:
        _list_to_check = list(list_to_check)
        if len(_list_to_check) == 0:
            raise eb.EmptyList
        elif len(_list_to_check) == 1:
            em.AssumeX()
            _list_to_check.extend([0, 0])
        elif len(_list_to_check) == 2:
            em.AssumeXY()
            _list_to_check.append(0)

        return _list_to_check
    except eb.EmptyList:
        em.EmptyList(3)
