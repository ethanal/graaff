# -*- coding: utf-8 -*-

# https://developers.google.com/maps/documentation/utilities/polylinealgorithm

import re

binary_matcher = re.compile(r"^[01]*$")


def invert(b):
    """Invert a binary string"""
    if binary_matcher.match(b) is None:
        raise ValueError("expected argument 1 to be a binary string")

    return "".join(str(int(not int(c))) for c in b)


def encode_float(f):
    if abs(f) > 180:
        raise ValueError("argument 1 must be between -180 and 180")

    b = bin(abs(int(round(f * 1e5))))[2:]
    b = ("0" * (32 - len(b))) + b

    if f < 0:
        b = invert(b)
        b = bin(int(b, 2) + 1)[2:]

    b = b[1:] + "0"

    if f < 0:
        b = invert(b)

    if len(b) % 5 != 0:
        b = "0" * (5 - (len(b) % 5)) + b

    chunks = [b[5 * s:5 * (s + 1)] for s in range(len(b) // 5)]
    while len(chunks) > 1 and chunks[0] == "00000":
        chunks.pop(0)

    chunks = chunks[::-1]
    or_with_0x20 = (lambda i, c: int(c, 2) | (0x20 * (i != len(chunks) - 1)))
    chunks = [or_with_0x20(i, c) for i, c in enumerate(chunks)]

    return "".join(chr(c + 63) for c in chunks)


def encode_polyline(points):
    # Convert any tuples to lists so they can be modified in place
    points = list(map(list, points))

    for i in reversed(range(len(points) - 1)):
        points[i + 1][0] -= points[i][0]
        points[i + 1][1] -= points[i][1]

    return "".join(encode_float(lo) + encode_float(la) for lo, la in points)
