"""
Created on Apr 14 23:59:42 2022
"""
from typing import Union

import numpy as np

np_arr = np.ndarray

FloatStr = Union[float, str]
FloatStrArr = Union[float, str, np_arr]


def change_instance(in_obj: FloatStr, in_type: str = 'dms') -> float:
    """
    Check if given input is DMS/HMS string and convert it to float.

    Parameters
    ----------
    in_obj : FloatStr
        Input object as HMS/DMS.
    in_type : str, optional
        Type of conversion. The default is 'dms'.

    Returns
    -------
    float
        DESCRIPTION.

    """
    if isinstance(in_obj, str):
        out = dms2dd(in_obj) if in_type == 'dms' else hms2dd(in_obj)
    else:
        out = in_obj

    return out


def altitude2zenith(altitude: FloatStrArr, deg_rad: bool = True) -> float:
    """
    Convert the given altitude to its complementary zenith angle.


    Parameters
    ----------
    altitude : FloatStrArr
        Altitude of the given celestial object.
    deg_rad : bool, optional
        Whether the given altitude measurement is in degrees or radians. Default is True.

    Returns
    -------
    float
        Complementary zenith angle for the corresponding altitude angle.

    """

    altitude = change_instance(altitude, 'dms')

    return 90 - altitude if deg_rad else np.pi / 2 - altitude


def zenith2altitude(zenith_angle: FloatStrArr, deg_rad: bool = True) -> float:
    """
    Convert the given zenith angle to its complementary altitude angle.

    Parameters
    ----------
    zenith_angle : FloatStrArr
        Zenith angle of the given celestial object.
    deg_rad : bool, optional
        Whether the given zenith angle measurement is in degrees or radians.
        The default is True.

    Returns
    -------
    float :
        Complementary altitude angle for the corresponding zenith angle.

    """

    zenith_angle = dms2dd(zenith_angle) if type(zenith_angle) == str else zenith_angle

    return 90 - zenith_angle if deg_rad else np.pi / 2 - zenith_angle


def dms2dd(dms: str) -> float:
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

    deg, minute, sec = [float(j) for j in dms.split(':')]

    # check for negative degree value
    if deg < 0:
        minute, sec = float(f'-{minute}'), float(f'-{sec}')

    return deg + minute / 60 + sec / 3600


def dd2dms(degree_decimal: float) -> str:
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

    if int(_s) == _s:
        _s = int(_s)

    return f'{int(_d)}:{int(_m)}:{_s}'


def hms2dd(hms: str) -> float:
    """
    Convert a given hour-minute-second string to degree decimal.


    Parameters
    ----------
    hms : str
        String representing the hour-minute-second value.

    Returns
    -------
    float
        Degree decimal value of the corresponding HMS input value.

    """

    hour, minute, sec = [float(i) for i in hms.split(':')]

    if hour < 0:
        print('RA value cannot be negative, assuming positive.')
        hour = -hour

    return hour * 15 + (minute / 4) + (sec / 240)


def dd2hms(degree_decimal: float) -> str:
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

    if int(_s) == _s:
        _s = int(_s)

    return f'{int(_d)}:{int(_m)}:{_s}'


def RA2HA(right_ascension: FloatStr, local_time: FloatStr) -> str:
    """
    Converts right ascension to its corresponding hour angle value depending upon the
    given local time.

    Parameters
    ----------
    right_ascension : FloatStr
        Right ascension value for the celestial object. It can either be a string with
        HH:MM:SS format or a float number representing the right ascension value.
    local_time : FloatStr
        Local time for the observer.

    Returns
    -------
    str
        Hour angle value of the object in the sky according to observer's local time.

    """

    _ra = change_instance(right_ascension, 'hms')
    _lt = change_instance(local_time, 'hms')

    if _ra > _lt:
        _lt += 360

    return dd2hms(_lt - _ra)


def HA2RA(hour_angle: FloatStrArr, local_time: FloatStr) -> str:
    """
    Converts hour angle to its corresponding right ascension value depending upon the
    given local time.

    Parameters
    ----------
    hour_angle : FloatStr
        Hour angle value for the celestial object.
    local_time : FloatStr
        Local time for the observer.

    Returns
    -------
    str
        Right ascension value of the object in the sky according to observer's local time.

    Notes
    -------
        The hour_angle and local_time parameters can either be a string with HH:MM:SS
        format or a float number representing the degree decimal representation of
        their values.
    """

    _ha = change_instance(hour_angle, 'hms')
    _lt = change_instance(local_time, 'hms')

    if _ha > _lt:
        _lt += 360

    return dd2hms(_lt - _ha)
