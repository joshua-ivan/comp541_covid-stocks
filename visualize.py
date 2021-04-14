import pandas, matplotlib
import config, util

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)
    data_frame = pandas.read_csv('Indices/Wilshire/$W5000.csv', usecols=['Date','Close'], index_col='Date')
    data_frame.index = pandas.to_datetime(data_frame.index, format="%Y%m%d")
    data_frame.plot()
    matplotlib.pyplot.savefig('/media/rock/DA67-61F9/test_fig.png')

if __name__ == "__main__":
    main()
