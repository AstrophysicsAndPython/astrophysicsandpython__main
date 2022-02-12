"""
Created on Thu Apr  1 01:12:40 2021
"""

import numpy as np


def coordinate_balance(x, y, value):
    if x > 0:
        if y > 0:
            value = value
        elif y < 0:
            value = 7 * value
    elif x < 0:
        if y > 0:
            value = 3 * value
        elif y < 0:
            value = 5 * value

    return np.abs(value)


def cartesian_spherical_converter(coordinates_3d, convert_to=None, deg_rad=None):
    """
    Converts Cartesian <=> Spherical coordinate system

    :param coordinates_3d: coordinates of the point in spherical or Cartesian system
    :param convert_to: string specifying either spherical/cartesian conversion
    :param deg_rad: whether the theta, phi parameters of spherical coordinates are in deg/rad units.
    :return: coordinates in covert_to coordinate system
    """
    if convert_to.lower() == 'spherical':
        # https://opentextbc.ca/calculusv3openstax/chapter/cylindrical-and-spherical-coordinates/
        x, y, z = coordinates_3d
        out1 = pow(pow(x, 2) + pow(y, 2) + pow(z, 2), 0.5)
        out2 = coordinate_balance(x, y, np.arctan(y / x))
        _num, _den = np.sqrt(pow(x, 2) + pow(y, 2)), z
        out3 = np.arctan(_num / _den)
    elif convert_to.lower() == 'cartesian':
        # https://tutorial.math.lamar.edu/classes/calciii/SphericalCoords.aspx
        rho, theta, phi = coordinates_3d
        if deg_rad == 'deg':
            theta, phi = np.radians(theta), np.radians(phi)
        out1 = rho * np.cos(theta) * np.sin(phi)
        out2 = rho * np.sin(theta) * np.sin(phi)
        out3 = rho * np.cos(phi)
    else:
        print('Please specify convert_to to either spherical or cartesian.')
        return None, None, None

    out1, out2, out3 = round(out1, 4), round(out2, 4), round(out3, 4)

    return out1, out2, out3
