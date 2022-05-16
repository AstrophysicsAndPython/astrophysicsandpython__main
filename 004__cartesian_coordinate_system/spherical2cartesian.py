"""
Created on May 12 22:47:36 2022
"""

import numpy as np


def spherical2cartesian(spherical_coordinates, deg_rad: str = 'rad'):
    """
    Converts spherical coordinates to Cartesian/rectangular coordinates.

    Parameters
    ----------
    spherical_coordinates:
        A tuple containing spherical coordinates.
    deg_rad: str, optional
        Indication whether the input coordinates are in degrees or radians. The default
        is 'rad'.

    Returns
    -------
    list:
        Cartesian coordinates of the input spherical coordinates.

    """

    # convert from degrees to radians (only theta and phi parameters)

    if deg_rad == 'deg':
        cs__ = np.deg2rad(spherical_coordinates[1:])
        cs_ = np.append(spherical_coordinates[0], cs__)
    else:
        cs_ = np.array(spherical_coordinates)

    # reinitialize the coordinates
    rho, theta, phi = cs_.flatten()

    # calculate the Cartesian coordinates
    x = rho * np.sin(phi) * np.cos(theta)
    y = rho * np.sin(phi) * np.sin(theta)
    z = rho * np.cos(phi)

    return x, y, z
