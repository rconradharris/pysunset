"""
Trigonometic Functions

The algorithm expresses angular units in degrees so we wrap the standard
library functions to do the necessary conversions from degrees to radians and
back.
"""
from math import sin, cos, tan, asin, acos, atan, degrees, radians


def _deg_to_rad(f):
    def inner(x):
        return f(radians(x))
    return inner

sin = _deg_to_rad(sin)
cos = _deg_to_rad(cos)
tan = _deg_to_rad(tan)

del _deg_to_rad


def _rad_to_deg(f):
    def inner(x):
        return degrees(f(x))
    return inner

asin = _rad_to_deg(asin)
acos = _rad_to_deg(acos)
atan = _rad_to_deg(atan)

del _rad_to_deg
