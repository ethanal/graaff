import unittest
from graaff.polyline import invert, encode_float, encode_polyline


class TestPolyline(unittest.TestCase):
    def test_invert(self):
        self.assertEqual(invert("0000000000"), "1111111111")
        self.assertEqual(invert("1111111111"), "0000000000")
        self.assertEqual(invert("1010101010"), "0101010101")
        self.assertEqual(invert("0100010010"), "1011101101")

        self.assertRaises(ValueError, invert, ("1110110ff0"))
        self.assertRaises(ValueError, invert, ("fdsjklsdjf"))

    def test_encode_float(self):
        self.assertEqual(encode_float(-179.9832104), "`~oia@")
        self.assertEqual(encode_float(38.5), "_p~iF")
        self.assertEqual(encode_float(-120.2), "~ps|U")

        self.assertRaises(ValueError, encode_float, (190))
        self.assertRaises(ValueError, encode_float, (-190))

    def test_encode_polyline(self):
        points = [(38.5, -120.2),
                  (40.7, -120.95),
                  (43.252, -126.453)]
        self.assertEqual(encode_polyline(points),
                         "_p~iF~ps|U_ulLnnqC_mqNvxq`@")

if __name__ == "__main__":
    unittest.main()
