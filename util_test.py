from unittest.mock import call, MagicMock
import unittest, os
import util

class TestUtil(unittest.TestCase):
    def test_nav_to_trading_data(self):
        os.chdir = MagicMock()
        util.nav_to_trading_data('test_data', 'stocks')
        os.chdir.assert_called_with('/'.join(['test_data', 'stocks']))

if __name__ == '__main__':
    unittest.main()
