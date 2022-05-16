"""
Created on May 12 22:49:49 2022
"""

import numpy as np

import error_utilities as e_utils


def translation_in_coordinates(change_in_coordinates, starting_point=(0, 0, 0),
                               deg_rad: str = 'rad'):
    """
    Calculates new coordinates of the point in spherical system given the translation
    in the object's coordinates.

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
    e_utils.ensure_positive([starting_point, change_in_coordinates])

    # the starting_point is taken in radians
    r1, theta1, phi1 = starting_point
    r2, theta2, phi2 = change_in_coordinates

    # convert theta and phi to radians if not already
    theta1, phi1 = np.radians([theta1, phi1]) if deg_rad == 'deg' else theta2, phi1
    theta2, phi2 = np.radians([theta2, phi2]) if deg_rad == 'deg' else theta2, phi2

    # make sure that theta does not exceed 360
    _theta1, _theta2 = e_utils.ensure_theta([theta1, theta2])

    # make sure that phi does not exceed 180
    _phi1, _phi2 = e_utils.ensure_phi([phi1, phi2])

    _changed = [sum(x) for x in zip((r1, theta1, phi1), (r2, theta2, phi2))]

    print(f'The starting coordinates of the point were {r1}, {np.degrees(_theta1)}, '
          f'{np.degrees(_phi1)} in degrees.\n'
          f'The new coordinates of the point are {_changed[0]}, '
          f'{np.degrees(_changed[1])}, {np.degrees(_changed[2])}')

    return _changed
