from unittest.mock import patch, MagicMock
import unittest
import aggregate_csvs, config

class TestAggregateCsvs(unittest.TestCase):
    @patch('aggregate_csvs.pandas')
    def test_read_csv(self, mock_pandas):
        expected_list = [(1, 2, 3, 4, 5), (6, 7, 8, 9, 10)]
        mock_pandas.read_csv.return_value = MagicMock()
        mock_pandas.read_csv.return_value.to_records.return_value = expected_list
        mock_csv = 'test.csv'

        actual_list = aggregate_csvs.read_csv(mock_csv)
        mock_pandas.read_csv.assert_called_with(mock_csv, usecols=config.summary_file_columns)
        mock_pandas.read_csv.return_value.to_records.assert_called_with(index=False)
        for n in range(len(expected_list)):
            self.assertCountEqual(expected_list[n], actual_list[n])

    @patch('aggregate_csvs.pandas')
    def test_write_csv(self, mock_pandas):
        aggregate_csvs.write_csv([])
        mock_pandas.DataFrame.from_records.assert_called_with([], columns=config.summary_file_columns)
        mock_pandas.DataFrame.from_records.return_value.to_csv.assert_called_with('aggregate.csv')

if __name__ == '__main__':
    unittest.main()
