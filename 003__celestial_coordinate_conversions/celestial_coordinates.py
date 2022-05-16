"""
Created on Sat Apr 10 15:29:25 2021
"""

from typing import Tuple, Union

import numpy as np

import conversion_utilities as utils
from conversion_errors import IncompleteArguments, OutputTypeError

FloatStr = Union[float, str]

_long_ncp = np.radians([122.93192])


def equatorial2horizontal(observer_latitude: FloatStr,
                          declination: FloatStr,
                          right_ascension: FloatStr = None,
                          hour_angle: FloatStr = None,
                          local_time: FloatStr = None,
                          output_parameter: str = 'altitude',
                          output_type: type = str) -> Union[Tuple[str, str],
                                                            Tuple[float, float]]:
    """
    Convert the given equatorial coordinates to horizontal coordinates.

    Parameters
    ----------
    observer_latitude : FloatStr
        Latitude of the observer.
    declination : FloatStr
        Declination of the celestial object.
    right_ascension : FloatStr, optional
        Right ascension of the celestial object. The default is None.
    hour_angle : FloatStr, optional
        Hour angle of the celestial object. The default is None.
    local_time : FloatStr, optional
        Local time for the observer. The default is None.
    output_parameter : str, optional
        Whether to give altitude or zenith angle as output. The default is 'altitude'.
    output_type : type
        Whether the output should be in string or float. Default is str.

    Raises
    ------
    OutputTypeError
        Raised if the output type is not 'altitude', 'zenith', or 'zenith angle'.
    IncompleteArguments
        Raised if the argument set is not complete.

    Returns
    -------
    Union[Tuple[str, str], Tuple[float, float]]
        Horizontal coordinates of the celestial object.

    """
    declination, latitude = [utils.change_instance(i) for i in
                             [declination, observer_latitude]]
    output_parameter = output_parameter.lower()

    if output_parameter not in ['altitude', 'zenith', 'zenith angle']:
        raise OutputTypeError('The output type must either be \'altitude\', \'zenith\','
                              ' or \'zenith angle\'.')

    if None not in [right_ascension, hour_angle]:
        print('Both right_ascension and hour_angle parameters are provided.\n'
              'Using hour_angle for calculations.')
        hour_angle = utils.change_instance(hour_angle, 'hms')

    if right_ascension is None and hour_angle is None:
        raise IncompleteArguments('Either right_ascension or hour_angle must be '
                                  'provided.')

    if None not in [right_ascension, hour_angle] and local_time is None:
        raise IncompleteArguments('right_ascension argument must be passed with '
                                  'local_time argument')

    if hour_angle is None:
        hour_angle = utils.RA2HA(right_ascension, local_time)
        hour_angle = utils.change_instance(hour_angle, 'hms')
    else:
        hour_angle = utils.change_instance(hour_angle, 'hms')

    latitude, hour_angle, declination = np.radians([latitude, hour_angle, declination])

    x = -np.sin(latitude) * np.cos(declination) * np.cos(hour_angle)
    x += np.cos(latitude) * np.sin(declination)

    y = np.cos(declination) * np.sin(hour_angle)

    azimuth = np.degrees(-np.arctan2(y, x))

    altitude = np.sin(latitude) * np.sin(declination)
    altitude += np.cos(latitude) * np.cos(declination) * np.cos(hour_angle)

    altitude = np.degrees(np.arcsin(altitude))

    alt = altitude if output_parameter == 'altitude' else utils.altitude2zenith(altitude)

    azimuth = 180 - azimuth if latitude < 0 else azimuth

    if output_type == str:
        azimuth, alt = [utils.dd2dms(i) for i in [azimuth, alt]]

    return azimuth, alt


def horizontal2equatorial(observer_latitude: FloatStr,
                          azimuth: FloatStr,
                          altitude: FloatStr = None,
                          local_time: FloatStr = None,
                          zenith_angle: FloatStr = None,
                          out: str = 'ha'):
    """
    Convert the given horizontal coordinates to equatorial coordinates.

    Parameters
    ----------
    observer_latitude : FloatStr
        Latitude of the observer.
    azimuth : FloatStr
        Azimuth value for the celestial object.
    altitude : FloatStr
        Altitude value for the celestial object.
    local_time : FloatStr, optional
        Local time for the observer. If specified, the output will be changed to RA.
        The default is None.
    zenith_angle : FloatStr, optional
        Zenith angle for the celestial object. If specified, it will be given preference
        over the altitude. The default is None.
    out : str, optional
        Whether to give hour angle or right ascension as the output. The default is
        'ha'. The default is 'ha'.

    Raises
    ------
    OutputTypeError
        Raised if the output type is not in 'ra', 'ha', 'right ascension' or hour angle'.

    Returns
    -------
    Tuple[str, str]
        Equatorial coordinates of the celestial object.

    """

    if out.lower() not in ['ha', 'ra', 'hour angle', 'right ascension']:
        raise OutputTypeError('The output type must either be \'ra\', \'ha\', '
                              '\'right ascension\' or \'hour angle\'.')

    if local_time is not None:
        if out.lower() in ['ha', 'hour angle']:
            print('local_time defined. The output will be changed to RA value.')
            out = 'ra'

    if altitude is None and zenith_angle is None:
        raise IncompleteArguments('Either zenith_angle or altitude must be provided.')

    lat, az, alt = [utils.change_instance(i, 'dms') for i in [observer_latitude, azimuth,
                                                              altitude]]

    if None not in [altitude, zenith_angle]:
        print('Both zenith_angle and altitude parameters are provided.\n'
              'Using zenith_angle for calculations.')
        zenith_angle = utils.change_instance(zenith_angle, 'dms')
    else:
        zenith_angle = utils.altitude2zenith(alt)

        zenith_angle = -zenith_angle if lat < 0 else zenith_angle

    _conv = [np.radians(i) for i in [zenith_angle, az, lat]]

    zenith_angle, azimuth, latitude = _conv

    declination = np.sin(latitude) * np.cos(zenith_angle)
    declination += np.cos(latitude) * np.sin(zenith_angle) * np.cos(azimuth)

    declination = np.arcsin(declination)

    _num = np.cos(zenith_angle) - np.sin(latitude) * np.sin(declination)
    _den = np.cos(latitude) * np.cos(declination)

    _ha = np.arccos(_num / _den)

    hour_angle = 2 * np.pi - _ha if np.logical_or(latitude > 0 > declination,
                                                  latitude < 0 < declination) else _ha

    declination, hour_angle = np.degrees([declination, hour_angle])

    if out in ['ra', 'right ascension']:
        hour_angle = utils.HA2RA(hour_angle=hour_angle, local_time=local_time)

    return utils.dd2hms(hour_angle), utils.dd2dms(declination)


def equatorial2ecliptic(right_ascension: FloatStr,
                        declination: FloatStr,
                        output_type: type = str,
                        ecliptic: FloatStr = 23.43927944) -> Union[Tuple[str, str],
                                                                   Tuple[float, float]]:
    """
    Convert equatorial coordinates of an object to corresponding ecliptic coordinates.

    Parameters
    ----------
    right_ascension : FloatStr
        Right ascension of the celestial object.
    declination : FloatStr
        Declination of the celestial object.
    output_type : type, optional
        Whether the output should be in string format DMS or in degree decimal.
        The default is str.
    ecliptic : FloatStr, optional
        The value for the obliquity of the ecliptic. The default is 23.43927944.

    Returns
    -------
    Union[Tuple[str, str], Tuple[float, float]]
        The ecliptic coordinates of the given equatorial coordinates.


    """

    ra = utils.change_instance(right_ascension, 'hms')
    dec = utils.change_instance(declination)
    ecliptic = utils.change_instance(ecliptic)

    ra, dec, ecliptic = [np.radians(i) for i in [ra, dec, ecliptic]]

    lat = np.sin(dec) * np.cos(ecliptic)
    lat -= np.cos(dec) * np.sin(ecliptic) * np.sin(ra)

    lat = np.arcsin(lat)

    _num = np.sin(ra) * np.cos(ecliptic)
    _num += np.tan(dec) * np.sin(ecliptic)

    _den = np.cos(ra)

    long = np.arctan2(_num, _den)

    lat, long = np.degrees([lat, long])

    if output_type == str:
        lat, long = utils.dd2dms(lat), utils.dd2dms(long)

    return lat, long


def ecliptic2equatorial(latitude: FloatStr,
                        longitude: FloatStr,
                        output_type: type = str,
                        ecliptic: FloatStr = 23.43927944) -> Union[Tuple[str, str],
                                                                   Tuple[float, float]]:
    """
    Convert ecliptic coordinates of an object to corresponding equatorial coordinates.


    Parameters
    ----------
    latitude : FloatStr
        Latitude of the celestial object.
    longitude : FloatStr
        Longitude of the celestial object.
    output_type : type, optional
        Whether the output should be in string format DMS or in degree decimal.
        The default is str.
    ecliptic : FloatStr, optional
        The value for the obliquity of the ecliptic. The default is 23.43927944.

    Returns
    -------
    Union[Tuple[str, str], Tuple[float, float]]
        The ecliptic coordinates of the given equatorial coordinates.

    """
    lat = utils.change_instance(latitude)
    long = utils.change_instance(longitude)
    ecliptic = utils.change_instance(ecliptic)

    lat, long, ecliptic = np.radians([lat, long, ecliptic])

    dec = np.sin(lat) * np.cos(ecliptic)
    dec += np.cos(lat) * np.sin(ecliptic) * np.sin(long)

    dec = np.arcsin(dec)

    _num = np.sin(long) * np.cos(ecliptic)
    _num -= np.tan(lat) * np.sin(ecliptic)

    _den = np.cos(long)

    _ra = np.arctan2(_num, _den)

    ra, dec = np.degrees([_ra, dec])

    if output_type == str:
        ra, dec = utils.dd2hms(ra), utils.dd2dms(dec)

    return ra, dec


def equatorial2galactic(right_ascension: FloatStr,
                        declination: FloatStr,
                        output_type: type = str,
                        _ra_gal: float = 192.85948,
                        _dec_gal: float = 27.12825) -> Union[Tuple[str, str],
                                                             Tuple[float, float]]:
    """
    Convert equatorial coordinates of a celestial object to galactic coordinates.

    Parameters
    ----------
    right_ascension : FloatStr,
        Right ascension of the celestial body.
    declination : FloatStr
        Declination of the celestial body.
    output_type : str
        Whether the output should be a string of DMS or in degree decimal format.
    _ra_gal : float
        Right ascension value for the galactic center. The default is 192.85948.
    _dec_gal : float
        Declination value for the galactic center. The default is 27.12825.

    Raises
    -------
    OutputTypeError:
        Raised when the output_type parameter is neither str nor float type.

    Returns
    -------
    Union[Tuple[str, str], Tuple[float, float]]
        Galactic coordinates (lat, long) of the input equatorial coordinates.

    """
    ra = utils.change_instance(right_ascension, 'hms')
    dec = utils.change_instance(declination)

    if output_type not in [str, float]:
        raise OutputTypeError('The output_type parameter must either be str or float.')

    ra, dec, _ra_gal, _dec_gal = np.radians([ra, dec, _ra_gal, _dec_gal])

    _num = np.cos(dec) * np.sin(ra - _ra_gal)

    _den = np.sin(dec) * np.cos(_dec_gal)
    _den -= np.cos(dec) * np.sin(_dec_gal) * np.cos(ra - _ra_gal)

    long = np.arctan2(_num, _den)

    lat = np.sin(dec) * np.sin(_dec_gal)
    lat += np.cos(dec) * np.cos(_dec_gal) * np.cos(ra - _ra_gal)

    lat = np.arcsin(lat)

    long, lat = np.degrees([long, lat])

    if output_type == str:
        long, lat = [utils.dd2dms(i) for i in [long, lat]]

    return long, lat


def galactic2equatorial(galactic_latitude: FloatStr,
                        galactic_longitude: FloatStr,
                        output_type: type = str,
                        _ra_ngp: float = 192.85948,
                        _dec_ngp: float = 27.12825) -> Union[Tuple[str, str],
                                                             Tuple[float, float]]:
    """
    Convert the equatorial coordinates of a celestial object to their galactic
    counterparts.

    Parameters
    ----------
    galactic_latitude : FloatStr
        Galactic latitude of the celestial object.
    galactic_longitude :
        Galactic longitude of the celestial object
    output_type : type
        Whether the equatorial coordinates should be in HMS/DMS string format or degree
        decimal format.
    _ra_ngp : float, optional
        Right ascension value for the North Galactic Pole. The default value if 192.85948.
    _dec_ngp : float, optional
        Declination value for the North Galactic Pole. The default value if 27.12825.

    Raises
    -------
    OutputTypeError:
        Raised when the output_type parameter is neither str nor float type.

    Returns
    -------
    Union[Tuple[str, str], Tuple[float, float]]
        Equatorial coordinates (RA, Dec) for the input galactic coordinates.

    """

    if output_type not in [str, float]:
        raise OutputTypeError('The output_type parameter must either be str or float.')

    b, long = [utils.change_instance(i) for i in [galactic_latitude, galactic_longitude]]

    b, long, _ra_ngp, _dec_ngp = np.radians([b, long, _ra_ngp, _dec_ngp])

    dec = np.sin(_dec_ngp) * np.sin(b)
    dec += np.cos(_dec_ngp) * np.cos(b) * np.cos(_long_ncp - long)

    dec = np.arcsin(dec)

    _num = np.cos(b) * np.sin(_long_ncp - long)
    _den = np.cos(_dec_ngp) * np.sin(b)
    _den -= np.sin(_dec_ngp) * np.cos(b) * np.cos(_long_ncp - long)

    ra = np.arctan2(_num, _den)

    ra, dec = np.degrees([ra, dec])

    if output_type == str:
        ra, dec = utils.dd2hms(ra), utils.dd2dms(dec)

    return ra, dec
