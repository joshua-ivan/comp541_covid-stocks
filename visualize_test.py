from unittest.mock import patch, ANY, MagicMock
import matplotlib, unittest
import config, visualize

class TestVisualize(unittest.TestCase):

    @patch('visualize.pandas')
    def test_read_index(self, mock_pandas):
        mock_file_path = 'test_path'
        visualize.read_index(mock_file_path)
        mock_pandas.read_csv.assert_called_with(mock_file_path, usecols=['Date','Close'], index_col='Date')
        mock_pandas.to_datetime.assert_called_with(ANY, format="%Y%m%d")

    @patch('visualize.read_index')
    def test_generate_index_chart(self, mock_read_index):
        visualize.generate_index_chart()
        mock_read_index.assert_called_with(config.index_file_name)

    @patch('visualize.matplotlib')
    def test_save_chart(self, mock_matplotlib):
        mock_filename = 'test_file'
        visualize.save_chart(mock_filename)
        mock_matplotlib.pyplot.savefig.assert_called_with('/'.join([config.chart_directory, mock_filename]))

if __name__ == '__main__':
    unittest.main()
