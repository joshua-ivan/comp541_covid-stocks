from insufficient_data_exception import InsufficientDataException
from unittest.mock import patch
import unittest

class TestInsufficientDataException(unittest.TestCase):
    @patch('insufficient_data_exception.config')
    def test_init(self, mock_config):
        mock_config.start_date = '2020-02-01'
        mock_config.end_date = '2021-02-01'
        mock_asset_name = 'test'

        mock_exception = InsufficientDataException(mock_asset_name)

        self.assertEqual(mock_exception.message,\
            '{0} has insufficient data for {1} to {2}; skipping.'\
            .format(mock_asset_name, mock_config.start_date, mock_config.end_date))
