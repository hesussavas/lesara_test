import unittest

from etl import _days_since_last_order, _longest_interval


class TestDaysSince(unittest.TestCase):
    def test_1_days_since(self):
        dates = ['2017-10-16']
        result = _days_since_last_order(dates)
        self.assertEqual(result, 1)

    def test_1_days_since_with_several_dates(self):
        dates = ['2016-09-17', '2017-09-17', '2017-10-16']
        result = _days_since_last_order(dates)
        self.assertEqual(result, 1)

    def test_10_days_since_with_several_dates(self):
        dates = ['2016-09-17', '2017-10-07']
        result = _days_since_last_order(dates)
        self.assertEqual(result, 10)

    def test_wrong_format(self):
        dates = ['2016/09/17', '2017/10/07']
        result = _days_since_last_order(dates)
        self.assertEqual(result, 0)


class TestLongestInterval(unittest.TestCase):
    def test_with_1_interval(self):
        dates = ['2017-10-01', '2017-10-02']
        result = _longest_interval(dates)
        self.assertEqual(result, 1)

    def test_with_several_intervals(self):
        dates = ['2017-10-01', '2017-10-02', '2017-10-20']
        result = _longest_interval(dates)
        self.assertEqual(result, 18)

    def test_wrong_format(self):
        dates = ['2016/09/17', '2017/10/07']
        result = _longest_interval(dates)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
