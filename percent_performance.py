from data_frame_builder import DataFrameBuilder
import pandas, matplotlib, os, sys
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

def write_summary_csv(rows, args):
    pandas.DataFrame(rows, columns=config.summary_file_columns)\
        .to_csv(config.summary_file_name.format(args[0], args[1]))

def process_asset(asset, exchange, index_name, index_data_frame):
    asset_name = asset.split('.')[0]
    asset_data_frame = build_percent_performance_data_frame(asset_name, '/'.join([exchange, asset]))
    asset_data_frame[asset_name] = asset_data_frame[asset_name] - index_data_frame[index_name]
    generate_chart(exchange, asset_name, asset_data_frame)
    return get_summary(asset_name, asset_data_frame)

def parse_command_line_args():
    usage_string = 'Usage: python3 {0} <exchange> <prefix>'.format(sys.argv[0])

    if not len(sys.argv) >= 3:
        sys.exit(usage_string)
        return

    exchange = sys.argv[1]
    if not exchange in config.exchanges:
        print('{0} is not a valid stock exchange.'.format(exchange))
        sys.exit(usage_string)
        return

    prefix = sys.argv[2].upper()
    if not prefix.isalpha():
        print('{0} is not a valid stock prefix. (alphabetic characters only)'.format(prefix))
        sys.exit(usage_string)
        return

    return [exchange, prefix]

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)

    wilshire_5000_data_frame = build_percent_performance_data_frame(\
        config.wilshire_5000_asset_name, config.wilshire_5000_file_name)
    nasdaq_comp_data_frame = build_percent_performance_data_frame(\
        config.nasdaq_comp_asset_name, config.nasdaq_comp_file_name)

    args = parse_command_line_args()
    asset_list = [x for x in os.listdir(args[0]) if x.startswith(args[1])]

    index_data_frame = None
    index_name = None
    if args[0] == 'NASDAQ':
        index_data_frame = build_percent_performance_data_frame(\
            config.nasdaq_comp_asset_name, config.nasdaq_comp_file_name)
        index_name = config.nasdaq_comp_asset_name
    else:
        index_data_frame = build_percent_performance_data_frame(\
            config.wilshire_5000_asset_name, config.wilshire_5000_file_name)
        index_name = config.wilshire_5000_asset_name

    summary_rows = []
    for asset in asset_list:
        summary_rows.append(\
            process_asset(asset, args[0], index_name, index_data_frame))

    write_summary_csv(summary_rows, args)

if __name__ == "__main__":
    main()
