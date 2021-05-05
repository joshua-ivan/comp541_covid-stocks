import config

class InsufficientDataException(Exception):
    def __init__(self, asset_name):
        self.asset_name = asset_name
        self.message = '{0} has insufficient data for {1} to {2}; skipping.'\
            .format(asset_name, config.start_date, config.end_date)
        super().__init__(self.message)

