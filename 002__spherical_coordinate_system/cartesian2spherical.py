"""
Created on Thu Apr  1 01:12:40 2021
"""

import numpy as np


def cartesian2spherical(rectangular_coordinates):
    """
    Converts Cartesian coordinates to spherical coordinates.

    Parameters
    ----------
    rectangular_coordinates:
        A list of coordinates of the point in Cartesian space.

    Returns
    -------
    list:
        Spherical coordinates of the input Cartesian coordinates.
    """

    # initialize the coordinates
    x, y, z = rectangular_coordinates

    # calculate rho
    rho = np.sqrt(x**2 + y**2 + z**2)

    # calculate theta, the reason for using arctan2 is that the range of theta
    # parameter is -180 < theta < 180.
    theta = np.arctan2(y, x)

    # calculate phi
    phi = np.arccos(z / rho)

    return rho, theta, phi
