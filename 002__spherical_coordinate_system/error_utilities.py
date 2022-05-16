"""
Created on May 12 22:13:09 2022
"""
from typing import Union

import numpy as np


class SphericalCoordinatesErrors(Exception):
    pass


class NegativeValueFound(SphericalCoordinatesErrors):
    pass


def ensure_theta(theta: Union[list, float]):
    # in part taken from https://stackoverflow.com/a/50457453
    return [x % (2 * np.pi) for x in theta] if isinstance(theta, list) else theta % (
            2 * np.pi)


def ensure_phi(phi: Union[list, float]):
    # in part taken from https://stackoverflow.com/a/50457453
    return [x % np.pi for x in phi] if isinstance(phi, list) else phi % np.pi


def ensure_positive(args):
    _sum = np.sum(args, axis=0)
    if any(x < 0 for x in _sum):
        raise NegativeValueFound('Found negative sum, these parameters can not have a '
                                 'negative sum.')
