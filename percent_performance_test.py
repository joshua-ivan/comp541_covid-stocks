from unittest.mock import patch, call, MagicMock
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

    @patch('percent_performance.matplotlib')
    @patch('percent_performance.os')
    def test_generate_chart(self, mock_os, mock_matplotlib):
        mock_frame = MagicMock()
        mock_filename = 'mock_chart'
        mock_directory = '/'.join([config.chart_directory, 'mock_exchange'])

        mock_os.path.isdir.side_effect = [True, True]
        percent_performance.generate_chart('mock_exchange', mock_filename, mock_frame)
        mock_frame.plot.assert_called()
        mock_os.path.isdir.assert_has_calls([call(config.chart_directory), call(mock_directory)])
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([mock_directory, mock_filename]))

        mock_os.path.isdir.side_effect = [False, False]
        percent_performance.generate_chart('mock_exchange', 'mock_chart', mock_frame)
        mock_frame.plot.assert_called()
        mock_os.mkdir.assert_has_calls([call(config.chart_directory), call(mock_directory)])
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([mock_directory, mock_filename]))

    @patch('percent_performance.generate_chart')
    @patch('percent_performance.build_percent_performance_data_frame')
    def test_process_asset(self, mock_build_df, mock_gen_chart):
        mock_exchange = 'MOCK'
        mock_asset_name = 'TEST'

        mock_asset_df = MagicMock()
        mock_build_df.return_value = mock_asset_df
        mock_index_df = MagicMock()

        percent_performance.process_asset('TEST.csv', mock_exchange, mock_exchange, mock_index_df)

        mock_build_df.assert_called_with(mock_asset_name, 'MOCK/TEST.csv')
        mock_gen_chart.assert_called_with(mock_exchange, mock_asset_name, mock_build_df.return_value)

    def test_get_summary(self):
        mock_asset_name = 'TEST'
        mock_data_frame = MagicMock()
        mock_data_frame[mock_asset_name][config.end_date] = .5
        mock_data_frame.stdev.return_value = {mock_asset_name: .1}

        summary = percent_performance.get_summary(mock_asset_name, mock_data_frame)
        self.assertEqual(summary,\
            [mock_asset_name, mock_data_frame[mock_asset_name][config.end_date], mock_data_frame.std()[mock_asset_name]])

    @patch('percent_performance.pandas')
    def test_write_summary_csv(self, mock_pandas):
        percent_performance.write_summary_csv([])
        mock_pandas.DataFrame.assert_called_with([], columns=config.summary_file_columns)
        mock_pandas.DataFrame.return_value.to_csv.assert_called_with(config.summary_file_name)

if __name__ == '__main__':
    unittest.main()
