========
pysunset
========

Computes the sunrise and sunset for a given location on a given date.

Uses the algorithm outlined here:

    http://williams.best.vwh.net/sunrise_sunset_algorithm.htm

Example
=======

::

    >>> import datetime, sunset
    >>> today = datetime.date.today()
    >>> lat, lng = 30.3, -96.27  # Austin, TX
    >>> utc_offset = -5 # CDT
    >>> sunset.get_sunset(today, lat, lng, utc_offset)
    datetime.datetime(2015, 4, 15, 19, 52, 33)
