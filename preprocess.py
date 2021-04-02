import os, sys, test, config

try:
    os.chdir('/'.join([config.dataset_name, config.path]))
except FileNotFoundError:
    sys.exit('Raw stock dataset not found. Run this next to the \"{0}\" directory.'\
        .format(config.dataset_name))
except NotADirectoryError:
    sys.exit('\"{0}\" is not a directory. Run this next to the raw stock dataset.'\
        .format(config.dataset_name))
except PermissionError:
    sys.exit('No permissions to change into the raw stock dataset on \"{0}/{1}\".'\
        .format(config.dataset_name, config.path))

full_path = os.getcwd().split('/')
directory_number = len(full_path)
test.greater_than_equal('Correct directory length', 3, directory_number)
actual_directory = '/'.join(full_path[directory_number - 3:])
test.equal('Correct working directory test', '/'.join([config.dataset_name, config.path]), actual_directory)

exchange_dirs = os.listdir()
for exchange in config.exchanges:
    test.is_true('Exchange directory presence test - {0}'.format(exchange), exchange in exchange_dirs)
    


