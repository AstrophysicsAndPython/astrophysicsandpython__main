"""
Created on Apr 14 23:59:42 2022
"""
from typing import Union

import numpy as np

np_arr = np.ndarray


def string_or_not(in_obj: Union[float, str], in_type: str = 'dms') -> float:
    """
    Check if given input is DMS/HMS string and convert it to float.

    Parameters
    ----------
    in_obj: Union[float, str]
        Input object as HMS/DMS.
    in_type: str
        Type of conversion. Default is 'dms'.

    Returns
    -------
    float:
        Degree decimal for the input dms/hms object.

    """
    if isinstance(in_obj, str):
        out = dms__dd(in_obj) if in_type == 'dms' else hms__dd(in_obj)
    else:
        out = in_obj

    return out


def altitude_to_zenith_angle(altitude: Union[float, str, np_arr], deg_rad: bool = True):
    """
    Convert the given altitude to its complementary zenith angle.


    Parameters
    ----------
    altitude : Union[float, str, np_arr]
        Altitude of the given celestial object.
    deg_rad : bool, optional
        Whether the given altitude measurement is in degrees or radians. Default is True.

    Returns
    -------
    object :
        Complementary zenith angle for the corresponding altitude angle.

    """

    altitude = dms__dd(altitude) if type(altitude) == str else altitude

    return 90 - altitude if deg_rad else np.pi / 2 - altitude


def zenith_angle_to_altitude(zenith_angle: Union[float, str, np_arr],
                             deg_rad: bool = True):
    """
    Convert the given zenith angle to its complementary altitude angle.

    Parameters
    ----------
    zenith_angle : Union[float, str, np_arr]
        Zenith angle of the given celestial object.
    deg_rad : bool, optional
        Whether the given zenith angle measurement is in degrees or radians.
        The default is True.

    Returns
    -------
    float
        Complementary altitude angle for the corresponding zenith angle.

    """

    zenith_angle = dms__dd(zenith_angle) if type(zenith_angle) == str else zenith_angle

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

    deg, minute, sec = [float(j) for j in dms.split(':')]

    # check for negative degree value
    if deg < 0:
        minute, sec = float(f'-{minute}'), float(f'-{sec}')

    return deg + minute / 60 + sec / 3600


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

    if int(_s) == _s:
        _s = int(_s)

    return f'{int(_d)}:{int(_m)}:{_s}'


def hms__dd(hms: str) -> float:
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

    if int(_s) == _s:
        _s = int(_s)

    return f'{int(_d)}:{int(_m)}:{_s}'


def RA_2_HA(right_ascension: Union[float, str], local_time: Union[float, str]) -> str:
    """
    Converts right ascension to its corresponding hour angle value depending upon the
    given local time.

    Parameters
    ----------
    right_ascension : Union[float, str]
        Right ascension value for the celestial object. It can either be a string with
        HH:MM:SS format or a float number representing the right ascension value.
    local_time : Union[float, str]
        Local time for the observer.

    Returns
    -------
    str
        Hour angle value of the object in the sky according to observer's local time.

    """

    _ra = hms__dd(right_ascension) if type(right_ascension) == str else right_ascension
    _lt = hms__dd(local_time) if type(local_time) == str else local_time

    if _ra > _lt:
        _lt += 360

    return dd__hms(_lt - _ra)


def HA_2_RA(hour_angle, local_time):
    """
    Converts hour angle to its corresponding right ascension value depending upon the
    given local time.

    Parameters
    ----------
    hour_angle : str, float
        Hour angle value for the celestial object. It can either be a string with
        HH:MM:SS format or a float number representing the hour angle value.
    local_time : str, float
        Local time for the observer.

    Returns
    -------
    str
        Right ascension value of the object in the sky according to observer's local time.

    """

    _ha = hms__dd(hour_angle) if type(hour_angle) == str else hour_angle
    _lt = hms__dd(local_time) if type(local_time) == str else local_time

    if _ha > _lt:
        _lt += 360

    return dd__hms(_lt - _ha)
