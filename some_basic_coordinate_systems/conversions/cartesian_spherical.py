"""
Created on Thu Apr  1 01:12:40 2021
"""

from typing import Tuple

import numpy as np


def spherical_to_cartesian(spherical_coordinates: Tuple[float, float, float], deg_rad: str = 'rad'):
    """
    Converts spherical coordinates to Cartesian/rectangular coordinates.

    Parameters
    ----------
    spherical_coordinates : Tuple[float, float, float]
        A tuple containing spherical coordinates.
    deg_rad : str, optional
        Indication whether the input coordinates are in degrees or radians. The default is 'rad'.

    Returns
    -------
    x : float
        x-coordinate of spherical coordinates.
    y : float
        y-coordinate in spherical coordinates.
    z : float
        z-coordinate in spherical coordinates.

    """

    cs_ = np.deg2rad(spherical_coordinates) if deg_rad == 'deg' else spherical_coordinates

    rho, theta, phi = cs_

    x = rho * np.sin(phi) * np.cos(theta)
    y = rho * np.sin(phi) * np.sin(theta)
    z = rho * np.cos(phi)

    return x, y, z


def cartesian_to_spherical(rectangular_coordinates, deg_rad='rad'):
    """


    Parameters
    ----------
    rectangular_coordinates : TYPE
        DESCRIPTION.
    deg_rad : TYPE, optional
        DESCRIPTION. The default is 'rad'.

    Returns
    -------
    rho : TYPE
        DESCRIPTION.
    theta : TYPE
        DESCRIPTION.
    phi : TYPE
        DESCRIPTION.

    """
    cs_ = np.deg2rad(rectangular_coordinates) if deg_rad == 'deg' else rectangular_coordinates

    x, y, z = cs_

    rho = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arccos(z / rho)

    return rho, theta, phi
