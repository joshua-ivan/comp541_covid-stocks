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

        mock_pandas.read_csv.assert_called_with(mock_asset_file, usecols=['Date','Close','Volume'], index_col='Date')
        builder_instance = mock_df_builder.return_value
        builder_instance.convert_index_to_datetime.assert_called_with("%Y%m%d")
        builder_instance.fill_missing_dates.assert_called()
        builder_instance.convert_to_percent_delta.assert_called_with('Close', '365D')
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
        mock_frame.plot.assert_called_with(xlabel='Date', ylabel='Performance %', secondary_y=['Volume'])
        mock_frame.plot.return_value.right_ax.set_ylabel.assert_called_with('Trade Volume')
        mock_os.path.isdir.assert_has_calls([call(config.chart_directory), call(mock_directory)])
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([mock_directory, mock_filename]))

        mock_os.path.isdir.side_effect = [False, False]
        percent_performance.generate_chart('mock_exchange', 'mock_chart', mock_frame)
        mock_frame.plot.assert_called_with(xlabel='Date', ylabel='Performance %', secondary_y=['Volume'])
        mock_frame.plot.return_value.right_ax.set_ylabel.assert_called_with('Trade Volume')
        mock_os.mkdir.assert_has_calls([call(config.chart_directory), call(mock_directory)])
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([mock_directory, mock_filename]))
        mock_matplotlib.pyplot.close.assert_called()

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
            [mock_asset_name,\
            mock_data_frame[mock_asset_name][config.end_date],\
            mock_data_frame[mock_asset_name].std(),\
            mock_data_frame['Volume'].mean(),\
            mock_data_frame['Volume'].std()])

    def _assert_csv_written(self, mock_pandas, mock_args):
        mock_pandas.DataFrame.assert_called_with([], columns=config.summary_file_columns)
        mock_pandas.DataFrame.return_value.to_csv.assert_called_with(\
            '/'.join([config.summary_file_directory, config.summary_file_name.format(mock_args[0], mock_args[1])]))

    @patch('percent_performance.pandas')
    @patch('percent_performance.os')
    def test_write_summary_csv(self, mock_os, mock_pandas):
        mock_args = ['MOCK', 'A']
        mock_os.path.isdir.return_value = True
        percent_performance.write_summary_csv([], mock_args)
        mock_os.path.isdir.assert_called()
        self._assert_csv_written(mock_pandas, mock_args)

        mock_os.path.isdir.return_value = False
        percent_performance.write_summary_csv([], mock_args)
        mock_os.mkdir.assert_called_with(config.summary_file_directory)
        self._assert_csv_written(mock_pandas, mock_args)

    def _assert_exit_called(self, mock_sys, usage_string):
        percent_performance.parse_command_line_args()
        mock_sys.exit.assert_called_with(usage_string)

    @patch('percent_performance.sys')
    @patch('percent_performance.config')
    @patch('builtins.print')
    def test_parse_command_line_args(self, mock_print, mock_config, mock_sys):
        mock_args = ['test', 'MOCK', 'A']
        mock_config.exchanges = ['MOCK']
        mock_sys.argv = mock_args
        args = percent_performance.parse_command_line_args()
        self.assertEqual(mock_args[1:], args)

        mock_sys.argv = ['test']
        usage_string = 'Usage: python3 {0} <exchange> <prefix>'.format(mock_sys.argv[0])
        self._assert_exit_called(mock_sys, usage_string)

        mock_sys.argv = ['test', 'MOCK']
        mock_config.exchanges = ['']
        self._assert_exit_called(mock_sys, usage_string)

        mock_sys.argv = ['test', 'MOCK', '1']
        mock_config.exchanges = ['MOCK']
        self._assert_exit_called(mock_sys, usage_string)

if __name__ == '__main__':
    unittest.main()
