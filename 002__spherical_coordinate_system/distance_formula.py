"""
Created on Thu Apr  1 03:05:09 2021
"""

from typing import List

import numpy as np

ListOfFloats = List[float, float, float]


def distance_formula(final_coordinates: ListOfFloats,
                     initial_coordinates: ListOfFloats = None,
                     deg_rad: str = 'rad') -> float:
    """
    Calculates the distance between two given points in spherical coordinate system
    Parameters
    ----------
    final_coordinates: List[float, float, float]
        Final coordinates of the point to which the distance is to be calculated.
    initial_coordinates: List[float, float, float]
        Reference coordinates of the point. The default is None.
    deg_rad: str, optional
        Whether the specified theta and phi arguments are in degree or radians.
        The default is 'rad'.

    Returns
    ----------
    float:
        Distance between two points in spherical coordinates
    """

    if initial_coordinates is None:
        initial_coordinates = [0, 0, 0]

    r1, theta1, phi1 = initial_coordinates
    r2, theta2, phi2 = final_coordinates

    theta1, phi1 = np.radians([theta1, phi1]) if deg_rad == 'deg' else theta2, phi1
    theta2, phi2 = np.radians([theta2, phi2]) if deg_rad == 'deg' else theta2, phi2

    p1 = r1**2 + r2**2

    _comp1 = np.sin(theta1) * np.sin(theta2) * np.cos(phi1 - phi2)
    _comp2 = np.cos(theta1) * np.cos(theta2)

    p2 = 2 * r1 * r2 * (_comp1 + _comp2)

    return np.sqrt(p1 - p2)
