#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:06:45 2021

@author: noonu
"""

import errors.error_base as eb
import errors.error_messages as em


def cartesian_2d(xy_distance: list, starting_point: list = None) -> list:

    try:
        if type(xy_distance) != list:
            raise eb.ListNotGiven
        if len(xy_distance) > 2:
            raise eb.ExtraParameterGiven
        if len(xy_distance) < 2:
            if len(xy_distance) == 0:
                raise eb.EmptyList
            elif len(xy_distance) == 1:
                em.AssumeX()
                xy_distance.append(0)
        if starting_point is None:
            starting_point = [0, 0]

        new_x_distance = starting_point[0] + xy_distance[0]
        new_y_distance = starting_point[1] + xy_distance[1]

        print(
            'The starting position of the object is {}.\n'
            'After moving <x: {}, y: {}> units, the new coordinates are '
            '<{}, {}>.'.format(
                starting_point, xy_distance[0], xy_distance[1], new_x_distance, new_y_distance
            )
        )

        return [new_x_distance, new_y_distance]

    except eb.ListNotGiven:
        em.ListNotGiven()
    except eb.ExtraParameterGiven:
        em.ExtraParameterGiven(2, len(xy_distance))
        return [None]*2
    except eb.EmptyList:
        em.EmptyList(2)
    except IndexError:
        print('The starting point must be a list with two values.')


def cartesian_3d(xyz_distance: [int, int, int], starting_point: [int, int] = None) -> [int, int, int]:

    try:
        if type(xyz_distance) != list:
            raise eb.ListNotGiven
        if len(xyz_distance) > 3:
            raise eb.ExtraParameterGiven
        if xyz_distance.__len__() < 3:
            if len(xyz_distance) == 0:
                raise eb.EmptyList
            elif len(xyz_distance) == 1:
                em.AssumeX()
                xyz_distance.extend([0, 0])
            elif len(xyz_distance) == 2:
                em.AssumeXY()
                xyz_distance.append(0)
        if starting_point is None:
            starting_point = [0, 0, 0]

        new_x_distance = starting_point[0] + xyz_distance[0]
        new_y_distance = starting_point[1] + xyz_distance[1]
        new_z_distance = starting_point[2] + xyz_distance[2]

        print(
            'The starting point of the object is {}.\n'
            'After moving <x: {}, y: {}, z: {}> units, the new coorindates '
            'are <{}, {}, {}>.'.format(
                starting_point, xyz_distance[0], xyz_distance[1], xyz_distance[2], new_x_distance, new_y_distance, new_z_distance
            )
        )

        return [new_x_distance, new_y_distance, new_z_distance]

    except eb.ListNotGiven:
        em.ListNotGiven()
    except eb.ExtraParameterGiven:
        em.ExtraParameterGiven(3, len(xyz_distance))
        return [None]*3
    except eb.EmptyList:
        em.EmptyList(3)
    except IndexError:
        print('The starting point must be a list with three values.')
