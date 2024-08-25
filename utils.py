
import pandas as pd

def parse_dates(dates):
    formatted_dates = []

    for date in dates:
        value = pd.NaT
        if pd.notna(date):
            try:
                value = pd.to_datetime(date, format='%Y-%m-%d', errors='raise').date()
            except ValueError:
                try:
                    value = pd.to_datetime(date, format='%m/%d/%Y', errors='raise').date()
                except ValueError:
                    pass
        formatted_dates.append(value)
    return pd.Series(formatted_dates)