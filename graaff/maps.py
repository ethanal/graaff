# -*- coding: utf-8 -*-

# https://developers.google.com/maps/documentation/staticmaps

from six import string_types, integer_types
from .exceptions import (
    InvalidGeographicCoordinateException, URLLengthException
)


class Map(object):
    _visible_locations = []
    _scale = None
    _height = None
    _width = None
    _map_type = None
    _format = None
    paths = []
    markers = []

    def add_visible_location(self, *args):
        invalid_args_msg = "expected 1 string argument or 2 numerical " \
                           "arguments."

        if len(args) == 1:
            # Address
            if not isinstance(args[0], string_types):
                raise TypeError(invalid_args_msg)
            self._visible_locations.append(args[0])
        elif len(args) == 2:
            # Geographical coordinate
            if not ((isinstance(args[0], float) or
                     isinstance(args[0], integer_types)) and
                    (isinstance(args[1], float) or
                     isinstance(args[1], integer_types))):
                raise TypeError(invalid_args_msg)
            self._visible_locations.append(",".join(map(str, args)))
        else:
            raise TypeError(invalid_args_msg)

    def add_path(self, path):
        self.paths.append(path)

    def add_marker(self, marker):
        self.markers.append(marker)

    def get_url(self, ignore_max_length=False):
        base_url = "https://maps.googleapis.com/maps/api/staticmap"
        url = base_url

        if not ignore_max_length and len(url) > 2048:
            raise URLLengthException("URL too long "
                                     "(length {})".format(len(url)))

    @property
    def visible_locations(self):
        return self._visible_locations

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def map_type(self):
        return self._map_type

    @map_type.setter
    def map_type(self, value):
        self._map_type = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value


class Marker(object):
    _size = None
    _color = None
    _label = None


class Path(object):
    color = None
    weight = None
    fill_color = None
    geodesic = None
    points = []

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            args_valid = [isinstance(a, tuple) for a in args]
            if args_valid.count(False) != 0:
                raise TypeError("expected all arguments to be tuples")

            valid_coordinates = [len(a) == 2 and
                                 abs(a[0]) <= 90 and
                                 abs(a[1]) <= 180 for a in args]
            if valid_coordinates.count(False) != 0:
                raise InvalidGeographicCoordinateException(
                    "invalid geographic coordinate at argument number " +
                    str(valid_coordinates.index(False) + 1)
                )

            for arg in args:
                self.points.append(*arg)
        # TODO Set kwargs

    def add_point(self, latitude, longitude):
        self.points.append((latitude, longitude))
