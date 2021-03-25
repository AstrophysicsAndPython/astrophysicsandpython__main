#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 18:19:25 2021

@author: noonu
"""

import errors.error_base as eb
import errors.error_messages as em


def number_line_with_direction(magnitude: int, starting_position: int = 0) -> int:

    try:
        if type(magnitude) != int:
            raise eb.IntNotPassed

        obj_position = starting_position + magnitude

        print(
            'The starting position of the object is {}.\n'
            'With a magnitude of {}, the final position of the object '
            'is {}.'.format(starting_position, magnitude, obj_position)
        )

        return obj_position

    except eb.IntNotPassed:
        em.IntNotPassed()

def number_line_no_direction(magnitude: int, starting_position: int = 0) -> [int, int]:

    try:
        if type(magnitude) != int:
            raise eb.IntNotPassed
        if magnitude < 0:
            raise eb.MagnitudeIsLessThanZero
        else:
            obj_position_positive = starting_position + magnitude
            obj_position_negative = starting_position - magnitude

            print(
                'The starting position is {}.\n'
                'With no direction specified, the object can have either'
                '{} or {} position.'.format(starting_position, obj_position_negative, obj_position_positive)
            )

        return [obj_position_positive, obj_position_negative]

    except eb.IntNotPassed:
        em.IntNotPassed()
    except eb.MagnitudeIsLessThanZero:
        em.MagnitudeIsLessThanZero()


def number_line_separate_direction(magnitude: int, direction: str, starting_position: int = 0) -> int:

    try:
        if type(magnitude) != int:
            raise eb.IntNotPassed
        if magnitude < 0:
            raise eb.MagnitudeIsLessThanZero
        if direction not in ['positive', 'negative']:
            raise eb.DirectionIsNotPosNeg
        else:
            if direction == 'negative':
                obj_position = starting_position - magnitude
            else:
                obj_position = starting_position + magnitude

            print(
                'The starting position of the object is {}.\n'
                'With a magnitude of {} and a {} direction, the current position is'
                ' {}.'.format(starting_position, magnitude, direction, obj_position)
            )

        return obj_position

    except eb.IntNotPassed:
        em.IntNotPassed()
    except eb.MagnitudeIsLessThanZero:
        em.MagnitudeIsLessThanZero()
    except eb.DirectionIsNotPosNeg:
        em.DirectionIsNotPosNeg()
