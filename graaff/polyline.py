# -*- coding: utf-8 -*-

# https://developers.google.com/maps/documentation/utilities/polylinealgorithm


def invert(b):
    """Invert a binary string"""
    return "".join(str(int(not int(c))) for c in b)


def encode_float(f):
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
    for i in reversed(range(len(points) - 1)):
        points[i + 1][0] -= points[i][0]
        points[i + 1][1] -= points[i][1]

    return "".join(encode_float(lo) + encode_float(la) for lo, la in points)
