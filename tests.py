from check_all_by_postal_code import get_ids, get_latlog
import unittest


class Tests(unittest.TestCase):
    def test_ids(self):
        result = get_ids("1111,2222")
        self.assertEqual(result, ["1111", "2222"])

    def test_get_latlog_supplied(self):
        myLat = 22
        myLong = 33
        report = False
        postal_code = None
        result = get_latlog(postal_code, myLat, myLong, report)
        self.assertEqual(result, (22, 33))

    def test_get_latlog_postal(self):
        myLat = None
        myLong = None
        report = False
        postal_code = "m5w1e6"
        result = get_latlog(postal_code, myLat, myLong, report)
        self.assertEqual(result, (43.683428, -79.392511))


if __name__ == "__main__":
    unittest.main()
