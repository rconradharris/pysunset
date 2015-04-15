"""
Algorithm for computing sunrise and sunset

This was ported from Javascript located at the source URL. No attempt was made
to perform any clean ups or refactoring, only the bare-minimum was done to
make the code run and the docstrings readable.

Source: http://www.esrl.noaa.gov/gmd/grad/solcalc/sunrise.html
"""
import datetime

import math

from utils import DMS_to_decimal

# Convert radian angle to degrees
def radToDeg(angleRad):
    return (180.0 * angleRad / math.pi)


# Convert degree angle to radians
def degToRad(angleDeg):
    return (math.pi * angleDeg / 180.0)


def calcJD(year, month, day):
    """Julian day from calendar day
    Arguments:
        year : 4 digit year
        month: January = 1
        day  : 1 - 31

    Return value:
      The Julian day corresponding to the date

    Note:
      Number is returned for start of day.  Fractional days should be
      added later.
    """
    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)

    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return JD;


def calcTimeJulianCent(jd):
    """Convert Julian Day to centuries since J2000.0

    Arguments:
        jd : the Julian Day to convert

    Return value:
        The T value corresponding to the Julian Day
    """
    T = (jd - 2451545.0) / 36525.0;
    return T


def calcJDFromJulianCent(t):
    """Convert centuries since J2000.0 to Julian Day.

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        the Julian Day corresponding to the t value
    """
    JD = t * 36525.0 + 2451545.0
    return JD


def calcGeomMeanLongSun(t):
    """Calculate the Geometric Mean Longitude of the Sun

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        the Geometric Mean Longitude of the Sun in degrees
    """
    L0 = 280.46646 + t * (36000.76983 + 0.0003032 * t)

    while (L0 > 360.0):
        L0 -= 360.0

    while (L0 < 0.0):
        L0 += 360.0

    return L0  # in degrees


def calcGeomMeanAnomalySun(t):
    """Calculate the Geometric Mean Anomaly of the Sun

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
      the Geometric Mean Anomaly of the Sun in degrees
    """
    M = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    return M  # in degrees


def calcEccentricityEarthOrbit(t):
    """Calculate the eccentricity of earth's orbit

    Arguments:
      t : number of Julian centuries since J2000.0

    Return value:
      the unitless eccentricity
    """
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    return e  # unitless


def calcSunEqOfCenter(t):
    """Calculate the equation of center for the sun

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        in degrees
    """
    m = calcGeomMeanAnomalySun(t)

    mrad = degToRad(m)
    sinm = math.sin(mrad)
    sin2m = math.sin(mrad + mrad)
    sin3m = math.sin(mrad + mrad + mrad)

    C = sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) + sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289
    return C  # in degrees


def calcSunTrueLong(t):
    """Calculate the true longitude of the sun

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        sun's true longitude in degrees
    """
    l0 = calcGeomMeanLongSun(t)
    c = calcSunEqOfCenter(t)

    O = l0 + c
    return O  # in degrees


def calcSunApparentLong(t):
    """Calculate the apparent longitude of the sun

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        sun's apparent longitude in degrees
    """
    o = calcSunTrueLong(t);

    omega = 125.04 - 1934.136 * t
    lambda_ = o - 0.00569 - 0.00478 * math.sin(degToRad(omega))
    return lambda_  # in degrees


def calcMeanObliquityOfEcliptic(t):
    """
    Calculate the mean obliquity of the ecliptic

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        mean obliquity in degrees
    """
    seconds = 21.448 - t * (46.8150 + t * (0.00059 - t * 0.001813))
    e0 = 23.0 + (26.0 + (seconds / 60.0)) / 60.0
    return e0  # in degrees


def calcObliquityCorrection(t):
    """
    Calculate the corrected obliquity of the ecliptic

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        corrected obliquity in degrees
    """
    e0 = calcMeanObliquityOfEcliptic(t);

    omega = 125.04 - 1934.136 * t;
    e = e0 + 0.00256 * math.cos(degToRad(omega));
    return e  # in degrees


def calcSunDeclination(t):
    """Calculate the declination of the sun

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        sun's declination in degrees
    """
    e = calcObliquityCorrection(t)
    lambda_ = calcSunApparentLong(t)

    sint = math.sin(degToRad(e)) * math.sin(degToRad(lambda_))
    theta = radToDeg(math.asin(sint))
    return theta  # in degrees


def calcEquationOfTime(t):
    """Calculate the difference between true solar time and mean solar time

    Arguments:
        t : number of Julian centuries since J2000.0

    Return value:
        equation of time in minutes of time
    """
    epsilon = calcObliquityCorrection(t)
    l0 = calcGeomMeanLongSun(t)
    e = calcEccentricityEarthOrbit(t)
    m = calcGeomMeanAnomalySun(t)

    y = math.tan(degToRad(epsilon)/2.0)
    y *= y

    sin2l0 = math.sin(2.0 * degToRad(l0))
    sinm   = math.sin(degToRad(m))
    cos2l0 = math.cos(2.0 * degToRad(l0))
    sin4l0 = math.sin(4.0 * degToRad(l0))
    sin2m  = math.sin(2.0 * degToRad(m))

    Etime = (y * sin2l0 - 2.0 * e * sinm + 4.0 * e * y * sinm * cos2l0
             - 0.5 * y * y * sin4l0 - 1.25 * e * e * sin2m)

    return radToDeg(Etime) * 4.0; # in minutes of time


def calcHourAngleSunrise(lat, solarDec):
    """Calculate the hour angle of the sun at sunrise for the latitude

    Arguments:
        lat : latitude of observer in degrees
        solarDec : declination angle of sun in degrees

    Return value:
        hour angle of sunrise in radians
    """
    latRad = degToRad(lat)
    sdRad  = degToRad(solarDec)

    HAarg = (math.cos(degToRad(90.833))/(math.cos(latRad)*math.cos(sdRad))-math.tan(latRad) * math.tan(sdRad));

    HA = (math.acos(math.cos(degToRad(90.833))/(math.cos(latRad)*math.cos(sdRad))-math.tan(latRad) * math.tan(sdRad)));

    return HA  # in radians


def calcHourAngleSunset(lat, solarDec):
    """Calculate the hour angle of the sun at sunset for the latitude

    Arguments:
        lat : latitude of observer in degrees
        solarDec : declination angle of sun in degrees

    Return value:
        hour angle of sunset in radians
    """
    latRad = degToRad(lat)
    sdRad  = degToRad(solarDec)

    HAarg = (math.cos(degToRad(90.833))/(math.cos(latRad)*math.cos(sdRad))-math.tan(latRad) * math.tan(sdRad))

    HA = (math.acos(math.cos(degToRad(90.833))/(math.cos(latRad)*math.cos(sdRad))-math.tan(latRad) * math.tan(sdRad)))

    return -HA  # in radians

def calcSunriseUTC(JD, latitude, longitude):
    """Calculate the Universal Coordinated Time (UTC) of sunrise for the given day
    at the given location on earth

    Arguments:
      JD  : julian day
      latitude : latitude of observer in degrees
      longitude : longitude of observer in degrees

    Return value:
      time in minutes from zero Z
    """
    t = calcTimeJulianCent(JD)

    # *** Find the time of solar noon at the location, and use
    #     that declination. This is better than start of the 
    #     Julian day

    noonmin = calcSolNoonUTC(t, longitude)
    tnoon = calcTimeJulianCent(JD+noonmin / 1440.0)

    # *** First pass to approximate sunrise (using solar noon)
    eqTime = calcEquationOfTime(tnoon)
    solarDec = calcSunDeclination(tnoon)
    hourAngle = calcHourAngleSunrise(latitude, solarDec)

    delta = longitude - radToDeg(hourAngle)
    timeDiff = 4 * delta  # in minutes of time
    timeUTC = 720 + timeDiff - eqTime  # in minutes

    # *** Second pass includes fractional jday in gamma calc

    newt = calcTimeJulianCent(calcJDFromJulianCent(t) + timeUTC / 1440.0)
    eqTime = calcEquationOfTime(newt)
    solarDec = calcSunDeclination(newt)
    hourAngle = calcHourAngleSunrise(latitude, solarDec)
    delta = longitude - radToDeg(hourAngle)
    timeDiff = 4 * delta
    timeUTC = 720 + timeDiff - eqTime # in minutes

    return timeUTC


def calcSolNoonUTC(t, longitude):
    """Calculate the Universal Coordinated Time (UTC) of solar noon for the
    given day at the given location on earth

    Arguments:
        t : number of Julian centuries since J2000.0
        longitude : longitude of observer in degrees

    Return value:
        time in minutes from zero Z
    """
    # First pass uses approximate solar noon to calculate eqtime
    tnoon = calcTimeJulianCent(calcJDFromJulianCent(t) + longitude / 360.0)
    eqTime = calcEquationOfTime(tnoon)
    solNoonUTC = 720 + (longitude * 4) - eqTime  # min

    newt = calcTimeJulianCent(calcJDFromJulianCent(t) - 0.5 + solNoonUTC / 1440.0)

    eqTime = calcEquationOfTime(newt)
    # var solarNoonDec = calcSunDeclination(newt);
    solNoonUTC = 720 + (longitude * 4) - eqTime  # min

    return solNoonUTC;


def calcSunsetUTC(JD, latitude, longitude):
    """Calculate the Universal Coordinated Time (UTC) of sunset for the given day
    at the given location on earth.

    Arguments:
        JD        : julian day
        latitude  : latitude of observer in degrees
        longitude : longitude of observer in degrees

    Return value:
        time in minutes from zero Z
    """
    t = calcTimeJulianCent(JD)

    # Find the time of solar noon at the location, and use that declination.
    # This is better than start of the # Julian day
    noonmin = calcSolNoonUTC(t, longitude)
    tnoon = calcTimeJulianCent (JD + noonmin / 1440.0)

    # First calculates sunrise and approx length of day
    eqTime = calcEquationOfTime(tnoon)
    solarDec = calcSunDeclination(tnoon)
    hourAngle = calcHourAngleSunset(latitude, solarDec)

    delta = longitude - radToDeg(hourAngle)
    timeDiff = 4 * delta
    timeUTC = 720 + timeDiff - eqTime

    # First pass used to include fractional day in gamma calc
    newt = calcTimeJulianCent(calcJDFromJulianCent(t) + timeUTC / 1440.0)
    eqTime = calcEquationOfTime(newt)
    solarDec = calcSunDeclination(newt)
    hourAngle = calcHourAngleSunset(latitude, solarDec)

    delta = longitude - radToDeg(hourAngle);
    timeDiff = 4 * delta;
    timeUTC = 720 + timeDiff - eqTime;  # in minutes

    return timeUTC

# Public functions

def get_sunrise(date, latitude, longitude, utc_offset, **kwargs):
    """Returns sunrise as a `datetime` or `None` if there is no sunrise for this
    location on the given date.

    date: `datetime.date` object representing the desired date
    latitude: latitidue in decimal degrees
    longitude: longitude in decimal degrees
    utc_offset: offset from UTC in hours (e.g. -5 is CDT)
    """
    # The NOAA algorithm uses positive values for west and negative values for
    # east. This is opposite the standard, so we reverse the longitude. (The
    # latitude sign is correct)
    longitude = -longitude

    year = date.year
    month = date.month
    day = date.day

    jd = calcJD(year, month, day)
    mins = calcSunriseUTC(jd, latitude, longitude)

    return (datetime.datetime(year, month, day) +
            datetime.timedelta(minutes=mins, hours=utc_offset))


def get_sunset(date, latitude, longitude, utc_offset, **kwargs):
    """Returns sunset as a `datetime` or `None` if there is no sunset for this
    location on the given date.

    date: `datetime.date` object representing the desired date
    latitude: latitidue in decimal degrees
    longitude: longitude in decimal degrees
    utc_offset: offset from UTC in hours (e.g. -5 is CDT)
    """
    # The NOAA algorithm uses positive values for west and negative values for
    # east. This is opposite the standard, so we reverse the longitude. (The
    # latitude sign is correct)
    longitude = -longitude

    year = date.year
    month = date.month
    day = date.day

    jd = calcJD(year, month, day)
    mins = calcSunsetUTC(jd, latitude, longitude)

    return (datetime.datetime(year, month, day) +
            datetime.timedelta(minutes=mins, hours=utc_offset))


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

    sunrise = get_sunrise(today, latitude, longitude, utc_offset)
    sunset = get_sunset(today, latitude, longitude, utc_offset)

    print(' '.join([
        "noaa".ljust(20),
        sunrise.strftime("%I:%M:%S %p").ljust(20),
        sunset.strftime("%I:%M:%S %p")
    ]))
