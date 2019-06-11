import pandas as pd
from shapely.wkb import loads


pd.set_option('display.expand_frame_repr', False)


def extract_coordinates_from_wkb_point(point):
    """
    Function extracting the coordinates from a well known byte hexadecimal string.

    :param point: Well known byte hexadecimal string describing a point.
    :type point: string
    :return: x and y coordinate of point.
    :rtype: touple of floats.
    """

    geometry = loads(point, hex=True)
    return geometry.x, geometry.y
