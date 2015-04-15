import datetime

import afc1990
import noaa
from utils import DMS_to_decimal


ALGORITHMS = {
    "afc1990": afc1990,
    "noaa": noaa
}


def get_sunrise(date, latitude, longitude, utc_offset, algorithm="afc1990", **kwargs):
    """Returns sunrise as a `datetime` or `None` if there is no sunrise for
    this location on the given date.

    date: `datetime.date` object representing the desired date
    latitude: latitude in decimal degrees (N is positive)
    longitude: longitude in decimal degrees (E is positive)
    utc_offset: offset from UTC in hours (e.g. -5 is CDT)
    algorithm: which algorithm to use
    """
    _get_sunrise = ALGORITHMS[algorithm].get_sunrise

    return _get_sunrise(date, latitude, longitude, utc_offset, **kwargs)


def get_sunset(date, latitude, longitude, utc_offset, algorithm="afc1990", **kwargs):
    """Returns sunset as a `datetime` or `None` if there is no sunset for this
    location on the given date.

    date: `datetime.date` object representing the desired date
    latitude: latitude in decimal degrees (N is positive)
    longitude: longitude in decimal degrees (E is positive)
    utc_offset: offset from UTC in hours (e.g. -5 is CDT)
    algorithm: which algorithm to use
    """
    _get_sunset = ALGORITHMS[algorithm].get_sunset

    return _get_sunset(date, latitude, longitude, utc_offset, **kwargs)


if __name__ == "__main__":
    today = datetime.date.today()

    # Position (Austin, TX)
    latitude = DMS_to_decimal(30, 16, 59)
    longitude = DMS_to_decimal(-97, -43, -59)
    utc_offset = -5  # CDT

    print(' '.join([
        'Algorithm'.ljust(20),
        'Sunrise'.ljust(20),
        'Sunset'
    ]))

    print("=" * 53)

    for algorithm in ('afc1990', 'noaa'):
        sunset = get_sunset(today, latitude, longitude, utc_offset,
                            algorithm=algorithm)

        sunrise = get_sunrise(today, latitude, longitude, utc_offset,
                              algorithm=algorithm)

        print(' '.join([
            algorithm.ljust(20),
            sunrise.strftime("%I:%M:%S %p").ljust(20),
            sunset.strftime("%I:%M:%S %p")
        ]))
