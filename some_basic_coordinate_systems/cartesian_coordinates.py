#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:06:45 2021

@author: noonu
"""

import errors.error_base as eb
import errors.error_messages as em
from some_basic_coordinate_systems.utilities import check_list_len_3d


def distance_formula_3d(initial_coordinates, final_coordinates):
    """
    Provides Euclidean distance between two points in 3 or less dimensional space.

    :param initial_coordinates: reference coordinates according to which the distance is to be calculated.
    :param   final_coordinates: position of the object in the space under observation
    :return                   : Euclidean distance between the two specified points

    Note: To use distance_formula_3d for 2D, specify z as 0 in both lists or only give 2 element list.
    """
    try:

        if type(initial_coordinates) != list or type(final_coordinates) != list:
            raise eb.ListNotGiven

        elif len(initial_coordinates) > 3 or len(final_coordinates) > 3:
            raise eb.ExtraParameterGiven

        if len(initial_coordinates) < 3:
            initial_coordinates = list(check_list_len_3d(initial_coordinates))

        if len(final_coordinates) < 3:
            final_coordinates = list(check_list_len_3d(final_coordinates))

        x1, y1, z1 = initial_coordinates
        x2, y2, z2 = final_coordinates

        out = round(pow(pow(x2 - x1, 2) + pow(y2 - y1, 2) + pow(z2 - z1, 2), 0.5), 4)

        print(f'The Euclidean distance between <{x1}, {y1}, {z1}> and <{x2}, {y2}, {z2}> is'
              f' {out}.')

        return out

    except eb.ListNotGiven:
        em.ListNotGiven()

    except eb.ExtraParameterGiven:
        em.ExtraParameterGiven(3)
        return None

    except TypeError:
        pass


def cartesian_3d(xyz_distance: [float, float, float], starting_point: [float, float, float] = None):
    """
    Provides Euclidean distance between two points in 3 or less dimensional space

    :param   xyz_distance: position of the point in the space under observation
    :param starting_point: reference coordinates according to which the new coordinates are to be calculated.
    :return              : New Cartesian coordinates for the point.

    :Note: To use cartesian_3d formula for 2D, specify z as 0 in both lists or only give 2 element list.
    """

    try:

        if type(xyz_distance) != list:
            raise eb.ListNotGiven

        elif len(xyz_distance) > 3:
            raise eb.ExtraParameterGiven

        elif len(xyz_distance) < 3:
            xyz_distance = list(check_list_len_3d(xyz_distance))

        if starting_point is None:
            starting_point = [0, 0, 0]

        x1, y1, z1 = xyz_distance

        new_x, new_y, new_z = [sum(x) for x in zip(starting_point, xyz_distance)]

        print(f'The starting point of the object is {starting_point}.\nAfter moving <{x1}, {y1}, {z1}> units, '
              f'the new coordinates are <{new_x}, {new_y}, {new_z}>')

        return [new_x, new_y, new_z]

    except eb.ListNotGiven:
        em.ListNotGiven()

    except eb.ExtraParameterGiven:
        em.ExtraParameterGiven(3, len(xyz_distance))
        return [None] * 3

    except IndexError:
        print('The starting point must be a list with three values.')
