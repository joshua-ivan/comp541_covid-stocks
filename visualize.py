import pandas, matplotlib, os
import config, util, data_frame_builder

def read_index(index_file_path):
    data_frame = pandas.read_csv(index_file_path, usecols=['Date','Close'], index_col='Date')
    data_frame.index = pandas.to_datetime(data_frame.index, format="%Y%m%d")

    data_frame = data_frame_builder.fill_missing_dates(data_frame)
    data_frame = data_frame_builder.convert_to_percent_delta(data_frame, '365D')
    data_frame = data_frame_builder.filter(data_frame, config.start_date, config.end_date)
    data_frame = data_frame_builder.rename_column(data_frame, 'Close', 'Wilshire 5000')
    data_frame = data_frame_builder.rename_axis(data_frame, 'columns', 'Percent Change')

    return data_frame

def generate_index_chart():
    index_frame = read_index(config.index_file_name)
    index_frame.plot()

def save_chart(filename):
    if not os.path.isdir(config.chart_directory):
        os.mkdir(config.chart_directory)
    matplotlib.pyplot.savefig('/'.join([config.chart_directory, filename]))

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)
    generate_index_chart()
    save_chart('test_fig.png')
    print('Chart saved to {0}.'.format('/'.join([config.dataset_name, config.path, config.chart_directory])))

if __name__ == "__main__":
    main()
