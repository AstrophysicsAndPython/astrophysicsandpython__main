#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 03:05:09 2021

@author: noonu
"""

import numpy as np


def distance_formula_spherical(initial_coordinates, final_coordinates=None, deg_rad=None):
    """

    Calculates the distance between two given points in spherical coordinate system

    :param initial_coordinates: reference coordinates of the point
    :param final_coordinates: final coordinates of the point to which the distance is to be calculated
    :param deg_rad: whether the specified theta and phi arguments are in degree or radians
    :return: distance between two points in spherical coordinates
    """

    r1, theta1, phi1 = initial_coordinates
    r2, theta2, phi2 = final_coordinates

    if deg_rad == 'deg':
        theta1, phi1, theta2, phi2 = np.radians(theta1), np.radians(phi1), np.radians(theta2), np.radians(phi2)

    _p1, _p2 = pow(r1, 2) + pow(r2, 2), - 2 * r1 * r2 * (np.sin(theta1) * np.sin(theta2) * np.cos(phi1 - phi2))
    _p3 = np.cos(theta1) * np.cos(theta2)

    return round(pow(_p1 + _p2 + _p3, 0.5), 4)


def spherical_3d(r_theta_phi_change, starting_point=None, deg_rad=None):
    """

    Calculates new location of the point in spherical coordinates system, given a translation of the object

    :param r_theta_phi_change: Change in the coordinates of the object given in a list in <r, theta, phi> order
    :param starting_point: Starting coordinates of the point in spherical coordinates
    :param deg_rad: whether the specified theta and phi arguments are in degree or radians
    :return: New coordinates for the point in spherical coordinate system
    """
    try:
        if starting_point is None:
            starting_point = [0, 0, 0]
        r, theta, phi = r_theta_phi_change
        if deg_rad == 'deg':
            theta, phi = np.radians(theta), np.radians(phi)

        r_theta_phi_change = [r, theta, phi]

        new_r, new_theta, new_phi = [sum(x) for x in zip(starting_point, r_theta_phi_change)]

        if 360 > np.degrees(new_theta) > 180:
            new_theta = np.radians(180 - (np.degrees(new_theta) - 180))
        elif -180 < np.degrees(new_theta) < 0:
            new_theta = np.abs(new_theta)

        if 0 < np.degrees(phi) < 90:
            direction_phi = 'N'
            direction_theta = 'W'
        elif 90 < np.degrees(phi) < 180:
            new_phi = np.radians(90 - (np.degrees(phi) - 90))
            direction_phi = 'N'
            direction_theta = 'W'
        elif 0 > np.degrees(phi) > -90:
            new_phi = np.abs(new_phi)
            direction_phi = 'S'
            direction_theta = 'E'
        elif -90 > np.degrees(phi) >= -180:
            print('im here')
            new_phi = np.radians(90 - (np.abs(np.degrees(phi)) - 90))
            direction_phi = 'S'
            direction_theta = 'W'
        else:
            print('Invalid input')

        print(f'The starting coordinates of the point are {starting_point}> in degrees.\n'
              f'The new coordinates of the point are <{new_r}, {np.degrees(new_theta)} {direction_theta}, '
              f'{np.degrees(new_phi)} {direction_phi}>')

        return round(new_r, 4), round(new_theta, 4), round(new_phi, 4)
    except UnboundLocalError:
        pass
