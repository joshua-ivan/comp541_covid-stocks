import pandas

class DataFrameBuilder:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def convert_index_to_datetime(self, f):
        self.data_frame.index = pandas.to_datetime(self.data_frame.index, format=f)

    def filter(self, start_date, end_date):
        self.data_frame = self.data_frame.loc[start_date:end_date]

    def rename_column(self, old_name, new_name):
        self.data_frame = self.data_frame.rename(columns = {old_name:new_name})

    def rename_axis(self, ax, name):
        self.data_frame = self.data_frame.rename_axis(name, axis=ax)

    def fill_missing_dates(self):
        self.data_frame = self.data_frame.resample('1D').ffill()

    def convert_to_percent_delta(self, f):
        self.data_frame = self.data_frame.pct_change(freq=f)

    def get_data_frame(self):
        return self.data_frame

