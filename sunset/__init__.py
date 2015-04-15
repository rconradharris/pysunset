"""
Higher-level API for accessing sunrise and sunset.

These APIs provide a Pythonic wrapper around the sunrise and sunset
calculation algorithm.

Datetime objects are used for time.
"""

import datetime

import algorithm
from utils import DMS_to_decimal


def _get_sunset_or_sunrise(mode, date, latitude, longitude, utc_offset,
                           zenith):
    day = date.day
    month = date.month
    year = date.year

    try:
        local_time_hours = algorithm.get_sunset_or_sunrise(
            mode, day, month, year, latitude, longitude, utc_offset, zenith)
    except (algorithm.NoSunrise, algorithm.NoSunset):
        return None

    return (datetime.datetime(year, month, day) +
            datetime.timedelta(hours=local_time_hours))


def get_sunrise(date, latitude, longitude, utc_offset, zenith='official'):
    """Returns sunrise as a `datetime` or `None` if there is no sunrise for
    this location on the given date.

    date: `datetime.date` object representing the desired date
    latitude: latitude in decimal degrees
    longitude: longitude in decimal degrees
    utc_offset: offset from UTC in hours (e.g. -5 is CDT)
    zenith: standard definition of sunrise ('official, 'civil', 'nautical',
            'astronomical')
    """
    return _get_sunset_or_sunrise('rising', date, latitude, longitude,
                                  utc_offset, zenith)


def get_sunset(date, latitude, longitude, utc_offset, zenith='official'):
    """Returns sunset as a `datetime` or `None` if there is no sunset for this
    location on the given date.

    date: `datetime.date` object representing the desired date
    latitude: latitidue in decimal degrees
    longitude: longitude in decimal degrees
    utc_offset: offset from UTC in hours (e.g. -5 is CDT)
    zenith: standard definition of sunset ('official, 'civil', 'nautical',
            'astronomical')
    """
    return _get_sunset_or_sunrise('setting', date, latitude, longitude,
                                  utc_offset, zenith)


if __name__ == "__main__":
    today = datetime.date.today()

    # Position (Austin, TX)
    latitude = DMS_to_decimal(30, 18, 0)
    longitude = DMS_to_decimal(-97, 44, 0)

    # UTC offset (CDT)
    utc_offset = -5

    print(' '.join([
        'Zenith Name'.ljust(20),
        'Sunrise'.ljust(20),
        'Sunset'
    ]))

    print("=" * 53)

    for zenith in ('official', 'civil', 'nautical', 'astronomical'):
        sunset = get_sunset(today, latitude, longitude, utc_offset, zenith)
        sunrise = get_sunrise(today, latitude, longitude, utc_offset, zenith)

        print(' '.join([
            zenith.ljust(20),
            sunrise.strftime("%I:%M:%S %p").ljust(20),
            sunset.strftime("%I:%M:%S %p")
        ]))
