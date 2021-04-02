from unittest.mock import MagicMock
import unittest, os
import preprocess, config

class TestPreprocess(unittest.TestCase):
    def test_nav_to_trading_data(self):
        os.chdir = MagicMock()
        preprocess.nav_to_trading_data(config.dataset_name, config.path)
        os.chdir.assert_called_with('/'.join([config.dataset_name, config.path]))

if __name__ == '__main__':
    unittest.main()
