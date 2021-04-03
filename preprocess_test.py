from unittest.mock import call, MagicMock
import unittest, os
import preprocess

class TestPreprocess(unittest.TestCase):
    def test_nav_to_trading_data(self):
        os.chdir = MagicMock()
        preprocess.nav_to_trading_data('test_data', 'stocks')
        os.chdir.assert_called_with('/'.join(['test_data', 'stocks']))

    def test_go(self):
        preprocess.filter_stocks = MagicMock()
        preprocess.go(['NYSE', 'NASDAQ'])
        preprocess.filter_stocks.assert_has_calls([call('NYSE'), call('NASDAQ')])

if __name__ == '__main__':
    unittest.main()
