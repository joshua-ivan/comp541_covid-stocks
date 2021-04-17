from unittest.mock import patch, ANY, MagicMock
import matplotlib, unittest, io
import config, visualize

class TestVisualize(unittest.TestCase):

    @patch('visualize.DataFrameBuilder')
    @patch('visualize.pandas')
    def test_read_index(self, mock_pandas, mock_df_builder):
        mock_file_path = 'test_path'

        data_frame = visualize.read_index(mock_file_path)

        mock_pandas.read_csv.assert_called_with(mock_file_path, usecols=['Date','Close'], index_col='Date')
        builder_instance = mock_df_builder.return_value
        builder_instance.convert_index_to_datetime.assert_called_with("%Y%m%d")
        builder_instance.fill_missing_dates.assert_called()
        builder_instance.convert_to_percent_delta.assert_called_with('365D')
        builder_instance.filter.assert_called_with(config.start_date, config.end_date)
        builder_instance.rename_column.assert_called_with('Close', 'Wilshire 5000')
        builder_instance.rename_axis.assert_called_with('columns', 'Percent Change')

    @patch('visualize.read_index')
    def test_generate_index_chart(self, mock_read_index):
        visualize.generate_index_chart()
        mock_read_index.assert_called_with(config.index_file_name)

    @patch('builtins.print')
    @patch('visualize.os')
    @patch('visualize.matplotlib')
    def test_save_chart(self, mock_matplotlib, mock_os, mock_print):
        mock_filename = 'test_file'

        mock_os.path.isdir.return_value = True
        visualize.save_chart(mock_filename)
        mock_os.path.isdir.assert_called_with(config.chart_directory)
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([config.chart_directory, mock_filename]))

        mock_os.path.isdir.return_value = False
        visualize.save_chart(mock_filename)
        mock_os.mkdir.assert_called_with(config.chart_directory)
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([config.chart_directory, mock_filename]))

if __name__ == '__main__':
    unittest.main()
