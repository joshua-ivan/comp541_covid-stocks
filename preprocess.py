import os, sys, test, config

def nav_to_trading_data(dataset_name, path):
    try:
        os.chdir('/'.join([dataset_name, path]))
    except FileNotFoundError:
        sys.exit('Raw stock dataset not found. Run this next to the \"{0}\" directory.'\
            .format(dataset_name))
    except NotADirectoryError:
        sys.exit('\"{0}\" is not a directory. Run this next to the raw stock dataset.'\
            .format(dataset_name))
    except PermissionError:
        sys.exit('No permissions to change into the raw stock dataset on \"{0}/{1}\".'\
            .format(dataset_name, path))

nav_to_trading_data(config.dataset_name, config.path)

exchange_dirs = os.listdir()
for exchange in config.exchanges:
    test.is_true('Exchange directory presence test - {0}'.format(exchange), exchange in exchange_dirs)
    


