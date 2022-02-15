"""
Created on Thu Apr  1 03:05:09 2021
"""

from typing import Tuple

import numpy as np

import utilities

TFloats = Tuple[float, float, float]


def distance_formula(initial_coordinates: TFloats, final_coordinates: TFloats = None, deg_rad: str = 'rad') -> float:
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

    return np.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * (np.sin(theta1) * np.sin(theta2) * np.cos(phi1 - phi2) + np.cos(theta1) * np.cos(theta2)))


def translation_in_coordinates(change_in_coordinates: TFloats, starting_point: TFloats = (0, 0, 0), deg_rad: str = 'rad'):
    """
    Calculates new coordinates of the point in spherical system given the translation in the object's coordinates.

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

    # make sure the sum of each individual argument is > 0
    utilities.ensure_positive([starting_point, change_in_coordinates])

    # the starting_point is taken in radians
    r1, theta1, phi1 = starting_point
    r2, theta2, phi2 = change_in_coordinates

    # convert theta and phi to radians if not already
    theta1, phi1, theta2, phi2 = np.radians([theta1, phi1, theta2, phi2]) if deg_rad == 'deg' else [theta1, phi1, theta2, phi2]

    # make sure that theta does not exceed 360
    _theta1, _theta2 = utilities.ensure_theta([theta1, theta2])

    # make sure that phi does not exceed 180
    _phi1, _phi2 = utilities.ensure_phi([phi1, phi2])

    _changed = [sum(x) for x in zip((r1, theta1, phi1), (r2, theta2, phi2))]

    print(f'The starting coordinates of the point were {r1}, {np.degrees(_theta1)}, {np.degrees(_phi1)} in degrees.\n'
          f'The new coordinates of the point are {_changed[0]}, {np.degrees(_changed[1])}, {np.degrees(_changed[2])}')

    return _changed
