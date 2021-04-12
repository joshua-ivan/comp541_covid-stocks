import os, sys

def nav_to_trading_data(dataset_name, path):
    try:
        os.chdir('/'.join([dataset_name, path]))
        return
    except FileNotFoundError:
        sys.exit('Raw stock dataset not found. Run this next to the \"{0}\" directory.'\
            .format(dataset_name))
    except NotADirectoryError:
        sys.exit('\"{0}\" is not a directory. Run this next to the raw stock dataset.'\
            .format(dataset_name))
    except PermissionError:
        sys.exit('No permissions to change into the raw stock dataset on \"{0}/{1}\".'\
            .format(dataset_name, path))

