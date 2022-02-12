"""
Created on Sat Apr 10 15:29:25 2021
"""

import numpy as np

import errors.error_base as eb
import errors.error_messages as em

_ecliptic, _ra_gal, _dec_gal, _long_ncp = np.radians([23.43927944, 192.85948, 27.12825, 122.93192])


def altitude__zenith_angle(altitude, deg=True):
    return 90 - altitude if deg else np.pi / 2 - altitude


def zenith_angle__altitude(zenith_angle, deg=True):
    return 90 - zenith_angle if deg else np.pi / 2 - zenith_angle


def right_ascension__hour_angle(right_ascension, local_time):
    _ra = dd__hms(right_ascension) if type(right_ascension) != str else float(right_ascension.split(':')[0])
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


def hour_angle__right_ascension(hour_angle, local_time):
    _ha = dd__hms(hour_angle) if type(hour_angle) != str else float(hour_angle.split(':')[0])
    _lt = dd__dms(local_time) if type(local_time) != str else float(local_time.split(':')[0])

    # if type(hour_angle) != str:
    #     hour_angle = dd__hms(hour_angle)
    # if type(local_time) != str:
    #     local_time = dd__dms(local_time)
    #
    # _ha = float(hour_angle.split(':')[0])
    # _lt = float(local_time.split(':')[0])

    if _ha > _lt:
        __ltm, __lts = local_time.split(':')[1:]
        local_time = f'{24 + _lt}:{__ltm}:{__lts}'

    return dd__dms(hms__dd(local_time) - hms__dd(hour_angle))


def dd__dms(degree_decimal):
    _d, __d = np.trunc(degree_decimal), degree_decimal - np.trunc(degree_decimal)

    __d = -__d if degree_decimal < 0 else __d

    _m, __m = np.trunc(__d * 60), __d * 60 - np.trunc(__d * 60)
    _s = round(__m * 60, 4)

    _s = int(_s) if int(_s) == _s else _s

    _m, _s = [_m + 1, '00'] if _s == 60 else [_m + 1, _s - 60]  # if _s > 60

    # if _s == 60:
    #     _m, _s = _m + 1, '00'
    # elif _s > 60:
    #     _m, _s = _m + 1, _s - 60

    return f'{int(_d)}:{int(_m)}:{_s}'


def dd__hms(degree_decimal):
    if type(degree_decimal) == str:
        degree_decimal = dms__dd(degree_decimal)
    if degree_decimal < 0:
        print('dd for HMS conversion cannot be negative, assuming positive.')
        _dd = -degree_decimal / 15
    else:
        _dd = degree_decimal / 15

    _h, __h = np.trunc(_dd), _dd - np.trunc(_dd)
    _m, __m = np.trunc(__h * 60), __h * 60 - np.trunc(__h * 60)
    _s = round(__m * 60, 4)

    _s = int(_s) if int(_s) == _s else _s

    _m, _s = [_m + 1, '00'] if _s == 60 else [_m + 1, _s - 60]

    # if _s == 60:
    #     _m, _s = _m + 1, '00'
    # elif _s > 60:
    #     _m, _s = _m + 1, _s - 60

    return f'{int(_h)}:{int(_m)}:{_s}'


def hms__dd(hms):
    try:
        _type = type(hms)
        hms, out = [[hms] if _type == str else hms][0], []

        for i in hms:
            if i[0] == '-':
                raise eb.HmsIsNegative()
            else:
                hour, minute, sec = i.split(':')
                hour, minute, sec = float(hour), float(minute), float(sec)

                out.append(hour * 15 + (minute / 4) + (sec / 240))

        return out[0] if _type == str or len(hms) == 1 else out
    except eb.HmsIsNegative:
        return em.HmsIsNegative()


def dms__dd(dms):
    dms, out = [dms] if type(dms) == str else dms, []

    for i in dms:
        deg, minute, sec = [float(j) for j in i.split(':')]
        if deg < 0:
            minute, sec = float(f'-{minute}'), float(f'-{sec}')

        out.append(deg + minute / 60 + sec / 3600)

    return out[0] if type(dms) == str or len(dms) == 1 else out


def equatorial__horizontal(observer_latitude, declination, right_ascension=None, hour_angle=None, local_time=None):
    declination, latitude = dms__dd([declination, observer_latitude])

    if right_ascension is not None:
        hour_angle = right_ascension__hour_angle(right_ascension, local_time)
        hour_angle = hms__dd(hour_angle)

    elif hour_angle is not None:
        hour_angle = hms__dd(hour_angle)

    elif right_ascension is not None and hour_angle is not None:
        print('Both right_ascension and hour_angle parameters are provided.\n'
              'Using hour_angle for calculations.')
        hour_angle = hms__dd(hour_angle)

    else:
        print('Either right_ascension or hour_angle must be provided.')

    latitude, hour_angle, declination = np.radians([latitude, hour_angle, declination])

    zenith_angle = np.arccos(np.sin(latitude) * np.sin(declination) + np.cos(latitude) * np.cos(declination) * np.cos(hour_angle))

    altitude = zenith_angle__altitude(zenith_angle, deg=False)

    _num = np.sin(declination) - np.sin(latitude) * np.cos(zenith_angle)
    _den = np.cos(latitude) * np.sin(zenith_angle)

    _az = np.arccos(_num / _den)

    azimuth = np.pi - _az if latitude < 0 else _az

    altitude, azimuth = np.degrees([altitude, azimuth])

    return dd__dms(altitude), dd__dms(azimuth)


def horizontal__equatorial(observer_latitude, altitude, azimuth):
    altitude, azimuth, latitude = np.radians([dms__dd([altitude, azimuth, observer_latitude])])

    zenith_angle = zenith_angle__altitude(altitude)

    zenith_angle = -zenith_angle if latitude < 0 else zenith_angle

    declination = np.arcsin(np.sin(latitude) * np.cos(zenith_angle) + np.cos(latitude) * np.sin(zenith_angle) * np.cos(azimuth))

    _num, _den = (np.cos(zenith_angle) - np.sin(latitude) * np.sin(declination), np.cos(latitude) * np.cos(declination))

    _ha = np.arccos(_num / _den)

    hour_angle = 2 * np.pi - _ha if np.logical_or(latitude > 0 > declination, latitude < 0 < declination) else _ha

    # if (latitude > 0 > declination) or (latitude < 0 < declination):
    #     hour_angle = 2 * np.pi - hour_angle

    declination, hour_angle = np.degrees([declination, hour_angle])

    return dd__dms(declination), dd__hms(hour_angle)


def equatorial__ecliptic(right_ascension, declination):
    ra, dec = hms__dd(right_ascension), dms__dd(declination)

    ec_latitude = np.arcsin(np.sin(dec) * np.cos(_ecliptic) - np.cos(dec) * np.sin(_ecliptic) * np.sin(ra))

    _num, _den = (np.sin(ra) * np.cos(_ecliptic) + np.tan(dec) * np.sin(_ecliptic), np.cos(ra))

    ec_longitude = np.arcsin(_num / _den)

    ec_latitude, ec_longitude = np.degrees([ec_latitude, ec_longitude])

    return dd__dms(ec_latitude), dd__dms(ec_longitude)


def ecliptic__equatorial(ecliptic_latitude, ecliptic_longitude):
    ec_latitude, ec_longitude = dms__dd([ecliptic_latitude, ecliptic_longitude])

    dec = np.arcsin(np.sin(ec_latitude) * np.cos(_ecliptic) + np.cos(ec_latitude) * np.sin(_ecliptic) * np.sin(ec_longitude))

    _num, _den = (np.cos(ec_latitude) * np.sin(ec_longitude) * np.cos(_ecliptic) -
                  np.sin(ec_latitude) * np.sin(_ecliptic), np.cos(ec_latitude) * np.cos(ec_longitude))

    _ra = np.arctan2(_num, _den)

    ra = _ra + 2 * np.pi if _ra < 0 else _ra

    # if ra < 0:
    #     ra = ra + 2 * np.pi

    ra, dec = np.degrees([ra, dec])

    return dd__hms(ra), dd__dms(dec)


def equatorial__galactic(right_ascension, declination):
    ra, dec = hms__dd(right_ascension), dms__dd(declination)

    gal_long = np.arctan2(np.cos(dec) * np.sin(ra - _ra_gal),
                          np.sin(dec) * np.cos(_dec_gal) - np.cos(dec) * np.sin(_dec_gal) * np.cos(ra - _ra_gal)) - _long_ncp

    gal_lat = np.arcsin(np.sin(dec) * np.sin(_dec_gal) + np.cos(dec) * np.cos(_dec_gal) * np.cos(ra - _ra_gal))

    gal_long, gal_lat = np.degrees([gal_long, gal_lat])

    return dd__dms(gal_long), dd__dms(gal_lat)


def galactic__equatorial(galactic_latitude, galactic_longitude):
    gal_lat, gal_long = dms__dd([galactic_latitude, galactic_longitude])

    dec = np.arcsin(np.sin(gal_lat) * np.sin(_dec_gal) + np.cos(gal_lat) * np.cos(_dec_gal) * np.cos(_long_ncp - gal_long))

    ra = np.arctan2(np.cos(gal_lat) * np.sin(_long_ncp - gal_long),
                    np.sin(gal_lat) * np.cos(_dec_gal) - np.cos(gal_lat) * np.sin(_dec_gal) * np.cos(_long_ncp - gal_long)) + _ra_gal

    ra, dec = np.degrees([ra, dec])

    return dd__hms(ra), dd__dms(dec)
