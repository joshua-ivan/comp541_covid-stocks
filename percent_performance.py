from data_frame_builder import DataFrameBuilder
import pandas, matplotlib, os
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

def generate_chart(exchange, chart_name, chart_frame):
    chart_frame.plot()

    if not os.path.isdir(config.chart_directory):
        os.mkdir(config.chart_directory)

    full_directory = '/'.join([config.chart_directory, exchange])
    if not os.path.isdir(full_directory):
        os.mkdir(full_directory)

    matplotlib.pyplot.savefig('/'.join([full_directory, chart_name]))

    matplotlib.pyplot.close()

def get_summary(asset_name, asset_data_frame):
    return [asset_name, asset_data_frame[asset_name][config.end_date], asset_data_frame.std()[asset_name]]

def write_summary_csv(rows):
    pandas.DataFrame(rows, columns=config.summary_file_columns).to_csv(config.summary_file_name)

def process_asset(asset, exchange, index_name, index_data_frame):
    asset_name = asset.split('.')[0]
    asset_data_frame = build_percent_performance_data_frame(asset_name, '/'.join([exchange, asset]))
    asset_data_frame[asset_name] = asset_data_frame[asset_name] - index_data_frame[index_name]
    generate_chart(exchange, asset_name, asset_data_frame)
    return get_summary(asset_name, asset_data_frame)

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)

    wilshire_5000_data_frame = build_percent_performance_data_frame(\
        config.wilshire_5000_asset_name, config.wilshire_5000_file_name)
    nasdaq_comp_data_frame = build_percent_performance_data_frame(\
        config.nasdaq_comp_asset_name, config.nasdaq_comp_file_name)

    summary_rows = []
    for exchange in config.exchanges:
        asset_list = os.listdir(exchange)
        for asset in asset_list:
            summary_rows.append(\
                process_asset(asset, exchange, config.wilshire_5000_asset_name, wilshire_5000_data_frame))

    asset_list = os.listdir('NASDAQ')
    for asset in asset_list:
        summary_rows.append(\
            process_asset(asset, exchange, config.nasdaq_comp_asset_name, nasdaq_comp_data_frame))

    write_summary_csv(summary_rows)

if __name__ == "__main__":
    main()
