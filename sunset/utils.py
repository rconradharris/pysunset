from __future__ import division
"""
Utility functions
"""

def DMS_to_decimal(degrees, minutes, seconds):
    """
    http://en.wikipedia.org/wiki/Decimal_degrees

    DD = D + M/60 + S/3600
    """
    return degrees + minutes / 60 + seconds / 3600
