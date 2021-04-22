import pandas, os
import config, util

def read_csv(file):
    df = pandas.read_csv(file, usecols=config.summary_file_columns)
    return list(df.to_records(index=False))

def write_csv(data):
    pandas.DataFrame.from_records(data, columns=config.summary_file_columns).to_csv('aggregate.csv')

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)

    csv_list = os.listdir(config.summary_file_directory)
    csv_aggregate = []
    for csv in csv_list:
        csv_aggregate += read_csv('/'.join([config.summary_file_directory, csv]))
    write_csv(csv_aggregate)

if __name__ == "__main__":
    main()
