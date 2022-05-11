"""
Created on Sat Apr 10 15:29:25 2021
"""

from typing import Tuple, Union

import numpy as np

import conversion_utilities as utils
from conversion_errors import IncompleteArguments, OutputTypeError

FloatStr = Union[float, str]

_ecliptic, _ra_gal, _dec_gal, _long_ncp = np.radians([23.43927944,
                                                      192.85948,
                                                      27.12825,
                                                      122.93192])


def equatorial__horizontal(observer_latitude: FloatStr,
                           declination: FloatStr,
                           right_ascension: FloatStr = None,
                           hour_angle: FloatStr = None,
                           local_time: FloatStr = None,
                           out: str = 'altitude') -> Tuple[str, str]:
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
    out : str, optional
        Whether to give altitude or zenith angle as output. The default is 'altitude'.

    Raises
    ------
    OutputTypeError
        Raised if the output type is not 'altitude', 'zenith', or 'zenith angle'.
    IncompleteArguments
        Raised if the argument set is not complete.

    Returns
    -------
    Tuple[str]
        Horizontal coordinates of the celestial object.

    """
    declination = utils.dms__dd(declination)
    latitude = utils.dms__dd(observer_latitude)
    out = out.lower()

    if out not in ['altitude', 'zenith', 'zenith angle']:
        raise OutputTypeError('The output type must either be \'altitude\', \'zenith\','
                              ' or \'zenith angle\'.')

    if None not in [right_ascension, hour_angle]:
        print('Both right_ascension and hour_angle parameters are provided.\n'
              'Using hour_angle for calculations.')
        hour_angle = utils.hms__dd(hour_angle) if type(hour_angle) == str else hour_angle

    if right_ascension is None and hour_angle is None:
        raise IncompleteArguments('Either right_ascension or hour_angle must be '
                                  'provided.')

    if None not in [right_ascension, hour_angle] and local_time is None:
        raise IncompleteArguments('right_ascension argument must be passed with '
                                  'local_time argument')

    if hour_angle is None:
        hour_angle = utils.hms__dd(utils.RA_2_HA(right_ascension, local_time))
    else:
        hour_angle = utils.hms__dd(hour_angle)

    latitude, hour_angle, declination = np.radians([latitude, hour_angle, declination])

    x = -np.sin(latitude) * np.cos(declination) * np.cos(hour_angle)
    x += np.cos(latitude) * np.sin(declination)

    y = np.cos(declination) * np.sin(hour_angle)

    azimuth = np.degrees(-np.arctan2(y, x))

    altitude = np.sin(latitude) * np.sin(declination)
    altitude += np.cos(latitude) * np.cos(declination) * np.cos(hour_angle)

    altitude = np.degrees(np.arcsin(altitude))

    alt = altitude if out == 'altitude' else utils.altitude_to_zenith_angle(altitude)

    _dir = 'E' if azimuth > 0 else 'W'

    azimuth = np.abs(azimuth)

    azimuth = 180 - azimuth if latitude < 0 else azimuth

    return f'{utils.dd__dms(azimuth)} {_dir}', utils.dd__dms(alt)


def horizontal__equatorial(observer_latitude: FloatStr,
                           azimuth: FloatStr,
                           altitude: FloatStr,
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
        Zenith angle for the celestial object. If specified, it will given preference
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

    lat, az, alt = [utils.string_or_not(i, 'dms') for i in [observer_latitude, azimuth,
                                                            altitude]]

    if None not in [altitude, zenith_angle]:
        print('Both zenith_angle and altitude parameters are provided.\n'
              'Using zenith_angle for calculations.')
        zenith_angle = utils.string_or_not(zenith_angle, 'dms')
    else:
        zenith_angle = utils.altitude_to_zenith_angle(alt)

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
        hour_angle = utils.HA_2_RA(hour_angle=hour_angle,
                                   local_time=local_time)

    return utils.dd__hms(hour_angle), utils.dd__dms(declination)


def equatorial__ecliptic(right_ascension, declination):
    ra, dec = utils.hms__dd(right_ascension), utils.dms__dd(declination)

    ec_latitude = np.arcsin(
            np.sin(dec) * np.cos(_ecliptic) - np.cos(dec) * np.sin(_ecliptic) * np.sin(
                    ra))

    _num, _den = (
        np.sin(ra) * np.cos(_ecliptic) + np.tan(dec) * np.sin(_ecliptic), np.cos(ra))

    ec_longitude = np.arcsin(_num / _den)

    ec_latitude, ec_longitude = np.degrees([ec_latitude, ec_longitude])

    return utils.dd__dms(ec_latitude), utils.dd__dms(ec_longitude)


def ecliptic__equatorial(ecliptic_latitude, ecliptic_longitude):
    ec_latitude = utils.dms__dd(ecliptic_latitude)
    ec_longitude = utils.dms__dd(ecliptic_longitude)

    dec = np.arcsin(
            np.sin(ec_latitude) * np.cos(_ecliptic) + np.cos(ec_latitude) * np.sin(
                    _ecliptic) * np.sin(ec_longitude))

    _num, _den = (np.cos(ec_latitude) * np.sin(ec_longitude) * np.cos(_ecliptic) -
                  np.sin(ec_latitude) * np.sin(_ecliptic),
                  np.cos(ec_latitude) * np.cos(ec_longitude))

    _ra = np.arctan2(_num, _den)

    ra = _ra + 2 * np.pi if _ra < 0 else _ra

    # if ra < 0:
    #     ra = ra + 2 * np.pi

    ra, dec = np.degrees([ra, dec])

    return utils.dd__hms(ra), utils.dd__dms(dec)


def equatorial__galactic(right_ascension, declination):
    ra, dec = utils.hms__dd(right_ascension), utils.dms__dd(declination)

    gal_long = np.arctan2(np.cos(dec) * np.sin(ra - _ra_gal),
                          np.sin(dec) * np.cos(_dec_gal) - np.cos(dec) * np.sin(
                                  _dec_gal) * np.cos(
                                  ra - _ra_gal)) - _long_ncp

    gal_lat = np.arcsin(
            np.sin(dec) * np.sin(_dec_gal) + np.cos(dec) * np.cos(_dec_gal) * np.cos(
                    ra - _ra_gal))

    gal_long, gal_lat = np.degrees([gal_long, gal_lat])

    return utils.dd__dms(gal_long), utils.dd__dms(gal_lat)


def galactic__equatorial(galactic_latitude, galactic_longitude):
    gal_lat, gal_long = [utils.dms__dd(i) for i in
                         [galactic_latitude, galactic_longitude]]

    dec = np.arcsin(
            np.sin(gal_lat) * np.sin(_dec_gal) + np.cos(gal_lat) * np.cos(
                    _dec_gal) * np.cos(_long_ncp - gal_long))

    ra = np.arctan2(np.cos(gal_lat) * np.sin(_long_ncp - gal_long),
                    np.sin(gal_lat) * np.cos(_dec_gal) - np.cos(gal_lat) * np.sin(
                            _dec_gal) * np.cos(
                            _long_ncp - gal_long)) + _ra_gal

    ra, dec = np.degrees([ra, dec])

    return utils.dd__hms(ra), utils.dd__dms(dec)
