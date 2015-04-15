========
pysunset
========

Computes the sunrise and sunset for a given location on a given date.

Uses the algorithm specified here:

    http://williams.best.vwh.net/sunrise_sunset_algorithm.htm


Examples
========

From Python::

    >>> import datetime, sunset
    >>> today = datetime.date.today()
    >>> lat, lng = 30.3, -96.27  # Austin, TX
    >>> utc_offset = -5 # CDT
    >>> sunset.get_sunset(today, lat, lng, utc_offset)
    datetime.datetime(2015, 4, 15, 19, 52, 33)


From the Command-Line::

    $ python sunset/__init__.py 
    Zenith Name          Sunrise              Sunset
    =====================================================
    official             06:58:12 AM          07:52:32 PM
    civil                06:33:36 AM          08:17:10 PM
    nautical             06:04:32 AM          08:46:16 PM
    astronomical         05:34:43 AM          09:16:08 PM
