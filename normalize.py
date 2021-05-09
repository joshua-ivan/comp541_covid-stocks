import percent_performance, util, config
import os, pandas

def process_asset(asset, exchange, index_performance):
    asset_name = asset.split('.')[0]
    asset_data_frame = percent_performance.build_percent_performance_data_frame(\
        asset_name, '/'.join([exchange, asset]))
    asset_data_frame[asset_name] = asset_data_frame[asset_name] - index_performance
    asset_data_frame.to_csv('/'.join([config.normalized_stock_directory, asset]))

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)

    comp_data_frame = percent_performance.build_percent_performance_data_frame(\
        config.nasdaq_comp_asset_name, config.nasdaq_comp_file_name)
    comp_name = config.nasdaq_comp_asset_name
    w5000_data_frame = percent_performance.build_percent_performance_data_frame(\
        config.wilshire_5000_asset_name, config.wilshire_5000_file_name)
    w5000_name = config.wilshire_5000_asset_name

    for exchange in config.exchanges:
        for asset in os.listdir(exchange):
            index_data_frame = w5000_data_frame
            index_name = w5000_name
            if exchange == 'NASDAQ':
                index_data_frame = comp_data_frame
                index_name = comp_name
            process_asset(asset, exchange, index_data_frame[index_name])

if __name__ == "__main__":
    main()
