"""
Created on Thu Apr  1 01:12:40 2021
"""

import numpy as np


def spherical_to_cartesian(spherical_coordinates, deg_rad: str = 'rad'):
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

    sc_ = spherical_coordinates

    # convert from degrees to radians (only theta and phi parameters)
    cs_ = np.append(sc_[0], np.deg2rad(sc_[1:])) if deg_rad == 'deg' else np.array(sc_)

    # reinitialize the coordinates
    rho, theta, phi = cs_.flatten()

    # calculate the Cartesian coordinates
    x = rho * np.sin(phi) * np.cos(theta)
    y = rho * np.sin(phi) * np.sin(theta)
    z = rho * np.cos(phi)

    return x, y, z


def cartesian_to_spherical(rectangular_coordinates):
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

    # calculate theta, the reason for using arctan2 is that the range of theta parameter is -180 < theta < 180.
    theta = np.arctan2(y, x)

    # calculate phi
    phi = np.arccos(z / rho)

    return rho, theta, phi
