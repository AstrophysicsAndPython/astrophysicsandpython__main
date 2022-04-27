"""
Created on Apr 14 23:59:42 2022
"""

import numpy as np


def altitude_to_zenith_angle(altitude, deg_rad: bool = True):
    """
    Convert the given altitude to its complementary zenith angle.


    Parameters
    ----------
    altitude :
        Altitude of the given celestial object.
    deg_rad : bool, optional
        Whether the given altitude measurement is in degrees. Default is True.

    Returns
    -------
    object :
        Complementary zenith angle for the corresponding altitude angle.

    """

    altitude, out = [altitude] if type(altitude) == float else altitude, []

    for alt in altitude:
        out.append(90 - alt if deg_rad else np.pi / 2 - alt)

    return out[0] if type(altitude) == float or len(altitude) == 1 else out


def zenith_angle_to_altitude(zenith_angle: float, deg_rad: bool = True) -> float:
    """
    Convert the given zenith angle to its complementary altitude angle.

    Parameters
    ----------
    zenith_angle : float
        Zenith angle of the given celestial object.
    deg_rad : bool, optional
        Whether the given altitude measurement is in degrees. The default is True.

    Returns
    -------
    float
        Complementary altitude angle for the corresponding zenith angle.

    """
    return 90 - zenith_angle if deg_rad else np.pi / 2 - zenith_angle


def dms__dd(dms: str) -> float:
    """
    Convert given degree minute second to degree decimal format.

    Parameters
    ----------
    dms : str
        String representing the degree-minute-second value.

    Returns
    -------
    float
        Degree decimal equivalent of the DMS input.

    Notes
    -------
        List conversion is possible

    """

    dms, out = [dms] if type(dms) == str else dms, []

    for i in dms:
        # split the string
        deg, minute, sec = [float(j) for j in i.split(':')]

        # check for negative degree value
        if deg < 0:
            minute, sec = float(f'-{minute}'), float(f'-{sec}')

        out.append(deg + minute / 60 + sec / 3600)

    return out[0] if type(dms) == str or len(dms) == 1 else out


def dd__dms(degree_decimal: float) -> str:
    """
    Convert given degree decimal format to degree minute seconds.


    Parameters
    ----------
    degree_decimal : float
        Degree decimal value.

    Returns
    -------
    str
        DMS equivalent of the input degree decimal value.

    """

    # get the truncated value
    _d = np.trunc(degree_decimal)

    # get the residual
    _deg_residual = abs(degree_decimal - _d)

    # get minutes
    __min = _deg_residual * 60
    _m = np.trunc(__min)

    # get the residual
    _min_residual = abs(__min - _m)

    # get seconds
    _s = round(_min_residual * 60, 4)

    _m, _s = [_m + 1, '00'] if _s == 60 else [_m, _s]

    return f'{int(_d)}:{int(_m)}:{_s}'


def hms__dd(hms: str) -> object:
    """
    Convert a given hour-minute-second string to degree decimal.


    Parameters
    ----------
    hms : str
        String representing the hour-minute-second value.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    hms, out = [hms] if type(hms) == str else hms, []

    for _hms in hms:
        hour, minute, sec = [float(i) for i in _hms.split(':')]

        out.append(hour * 15 + (minute / 4) + (sec / 240))

    return out[0] if type(hms) == str or len(hms) == 1 else out


def dd__hms(degree_decimal: float) -> str:
    """
    Convert degree decimal to its corresponding HMS notation.

    Parameters
    ----------
    degree_decimal : float
        Degree decimal value for the position of the object.

    Returns
    -------
    str
        Corresponding HMS value for the input DD value.

    """

    if degree_decimal < 0:
        print('dd for HMS conversion cannot be negative, assuming positive.')
        _dd = -degree_decimal / 15
    else:
        _dd = degree_decimal / 15

    # get the truncated value
    _d = np.trunc(_dd)

    # get the residual
    _deg_residual = abs(_dd - _d)

    # get minutes
    __min = _deg_residual * 60
    _m = np.trunc(__min)

    # get the residual
    _min_residual = abs(__min - _m)

    # get seconds
    _s = round(_min_residual * 60, 4)

    _m, _s = [_m + 1, '00'] if _s == 60 else [_m, _s]

    return f'{int(_d)}:{int(_m)}:{_s}'


def right_ascension__hour_angle(right_ascension, local_time):
    _ra = dd__hms(right_ascension) if type(right_ascension) != str else float(
            right_ascension.split(':')[0])
    _lt = dd__dms(local_time) if type(local_time) != str else float(local_time.split(':'))

    # if type(right_ascension) != str:
    #     right_ascension = dd__hms(right_ascension)
    # if type(local_time) != str:
    #     local_time = dd__dms(local_time)
    #
    # _ra = float(right_ascension.split(':')[0])
    # _lt = float(local_time.split(':')[0])

    if _ra > _lt:
        __ltm, __lts = local_time.split(':')[1:]
        local_time = f'{24 + _lt}:{__ltm}:{__lts}'

    return dd__dms(hms__dd(local_time) - hms__dd(right_ascension))
