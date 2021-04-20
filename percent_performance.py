from data_frame_builder import DataFrameBuilder
import pandas
import config, util

def build_percent_performance_data_frame(asset_name, asset_file):
    data_frame_builder = DataFrameBuilder(pandas.read_csv(asset_file, usecols=['Date','Close'], index_col='Date'))

    data_frame_builder.convert_index_to_datetime('%Y%m%d')
    data_frame_builder.fill_missing_dates()
    data_frame_builder.convert_to_percent_delta('365D')
    data_frame_builder.filter(config.start_date, config.end_date)
    data_frame_builder.rename_column('Close', asset_name)
    data_frame_builder.rename_axis('columns', 'Percent Change')

    return data_frame_builder.get_data_frame()

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)
    wilshire_5000_data_frame = build_percent_performance_data_frame('Wilshire 5000', config.wilshire_5000_file_name)
    nasdaq_comp_data_frame = build_percent_performance_data_frame('NASDAQ Composite Index', config.nasdaq_comp_file_name)

if __name__ == "__main__":
    main()
