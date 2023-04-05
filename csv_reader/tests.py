import unittest
from csv_reader import parse_csv


class Tests(unittest.TestCase):
    def test_ints(self):
        result = parse_csv(["one,two,three", "1,2,3"])
        self.assertEqual(result, {"one": [1], "two": [2], "three": [3]})

    def test_floats(self):
        result = parse_csv(["one,two,three", "1.0,2.2,3.3"])
        self.assertEqual(result, {"one": [1.0], "two": [2.2], "three": [3.3]})

    def test_int_float_mix(self):
        result = parse_csv(["one", "1.0", "1.2", "1"])
        self.assertEqual(result, {"one": ["1.0", "1.2", "1"]})

    def test_int_arrays(self):
        result = parse_csv(["one", "1|1|2|3"])
        self.assertEqual(result, {"one": [[1, 1, 2, 3]]})

    def test_arrays_none(self):
        result = parse_csv(["one", "1||||1"])
        self.assertEqual(result, {"one": [[1, None, None, None, 1]]})

    def test_arrays_none_mk2(self):
        result = parse_csv(["one,two", "None,None"])
        self.assertEqual(result, {"one": [None], "two": [None]})

    def test_arrays_float(self):
        result = parse_csv(["one", "5.5|3.4"])
        self.assertEqual(result, {"one": [[5.5, 3.4]]})

    def test_pure_nones(self):
        result = parse_csv(["one", ""])
        self.assertEqual(result, {"one": [None]})

    def test_empty_csv(self):
        result = parse_csv([""])
        self.assertEqual(result, {})

    def test_empty_csv_mk2(self):
        result = result = parse_csv([])
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
