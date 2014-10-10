# -*- coding: utf-8 -*-


class URLLengthException(Exception):
    """The URL generated was too long and will result in a 400 Bad
    Request Error if fetched"""
    pass


class InvalidGeographicCoordinateException(Exception):
    """An invalid latitude-longitude pair was specified."""
    pass
