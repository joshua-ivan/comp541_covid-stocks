from unittest.mock import call, MagicMock
import unittest, os
import preprocess

class TestPreprocess(unittest.TestCase):
    def test_go(self):
        preprocess.filter_stocks = MagicMock()
        preprocess.go(['NYSE', 'NASDAQ'])
        preprocess.filter_stocks.assert_has_calls([call('NYSE'), call('NASDAQ')])

if __name__ == '__main__':
    unittest.main()
