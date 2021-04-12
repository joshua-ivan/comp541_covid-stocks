import config, util

def filter_stocks(exchange):
    print(exchange)
    return

def go(exchanges):
    for exchange in exchanges:
        filter_stocks(exchange)
    return

def main():
    util.nav_to_trading_data(config.dataset_name, config.path)
    go(config.exchanges)

if __name__ == "__main__":
    main()
