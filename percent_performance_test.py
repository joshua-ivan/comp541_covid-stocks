from unittest.mock import patch, MagicMock
import unittest
import percent_performance, config

class TestPercentPerformance(unittest.TestCase):

    @patch('percent_performance.DataFrameBuilder')
    @patch('percent_performance.pandas')
    def test_build_percent_performance_data_frame(self, mock_pandas, mock_df_builder):
        mock_asset_name = 'test_asset'
        mock_asset_file = 'test_path'

        data_frame = percent_performance.build_percent_performance_data_frame(mock_asset_name, mock_asset_file)

        mock_pandas.read_csv.assert_called_with(mock_asset_file, usecols=['Date','Close'], index_col='Date')
        builder_instance = mock_df_builder.return_value
        builder_instance.convert_index_to_datetime.assert_called_with("%Y%m%d")
        builder_instance.fill_missing_dates.assert_called()
        builder_instance.convert_to_percent_delta.assert_called_with('365D')
        builder_instance.filter.assert_called_with(config.start_date, config.end_date)
        builder_instance.rename_column.assert_called_with('Close', mock_asset_name)
        builder_instance.rename_axis.assert_called_with('columns', 'Percent Change')

if __name__ == '__main__':
    unittest.main()
