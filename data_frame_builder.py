def filter(df, start_date, end_date):
    return df.loc[start_date:end_date]

def rename_column(df, old_name, new_name):
    return df.rename(columns = {old_name:new_name})

def rename_axis(df, ax, name):
    return df.rename_axis(name, axis=ax)
