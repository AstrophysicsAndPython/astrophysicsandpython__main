"""
Created on Thu Apr  1 03:05:09 2021
"""

from typing import List

import numpy as np

ListOfFloats = List[float, float, float]


def distance_formula_spherical(initial_coordinates: ListOfFloats, final_coordinates: ListOfFloats = None, deg_rad: str = None) -> float:
    """
    Calculates the distance between two given points in spherical coordinate system

    Parameters
    ----------
    initial_coordinates:
        Reference coordinates of the point
    final_coordinates:
        Final coordinates of the point to which the distance is to be calculated
    deg_rad:
        Whether the specified theta and phi arguments are in degree or radians

    Returns
    ----------
    float:
        Distance between two points in spherical coordinates
    """

    r1, theta1, phi1 = initial_coordinates
    r2, theta2, phi2 = final_coordinates

    theta1, phi1, theta2, phi2 = np.radian([theta1, phi1, theta2, phi2]) if deg_rad == 'deg' else [theta2, phi1, theta2, phi2]

    _frac1 = pow(r1, 2) + pow(r2, 2)
    _frac2 = - 2 * r1 * r2 * (np.sin(theta1) * np.sin(theta2) * np.cos(phi1 - phi2))
    _frac3 = np.cos(theta1) * np.cos(theta2)

    return pow(_frac1 + _frac2 + _frac3, 0.5)


def spherical_3d(change_in_coordinates: ListOfFloats, starting_point: ListOfFloats = None, deg_rad: str = None):
    """
    Calculates new location of the point in spherical coordinates system, given a translation of the object

    Parameters
    ----------
    change_in_coordinates:
        Change in the coordinates of the object given in a list in <r, theta, phi> order
    starting_point:
        Starting coordinates of the point in spherical coordinates.
    deg_rad:
        Whether the specified theta and phi arguments are in degree or radians

    Returns
    ----------
    float:
        New coordinates for the point in spherical coordinate system
    """
    try:

        r, theta, phi = change_in_coordinates

        starting_point = [0, 0, 0] if starting_point is None else starting_point

        theta, phi = np.radians([theta, phi]) if deg_rad == 'deg' else [theta, phi]

        change_in_coordinates = [r, theta, phi]

        new_r, new_theta, new_phi = [sum(x) for x in zip(starting_point, change_in_coordinates)]

        if 360 > np.degrees(new_theta) > 180:
            new_theta = np.radians(180 - (np.degrees(new_theta) - 180))
        elif -180 < np.degrees(new_theta) < 0:
            new_theta = np.abs(new_theta)

        # have to check this out
        #
        # (direction_phi, direction_theta) = [('N', 'W') if 0 < np.degrees(phi) < 90 else
        #                                     ('N', 'E') if 90 < np.degrees(phi) < 80 else
        #                                     ('S', 'E') if 0 > np.degrees(phi) > -90 else
        #                                     ('S', 'W') if -90 > np.degrees(phi) >= 180 else None][0]

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
