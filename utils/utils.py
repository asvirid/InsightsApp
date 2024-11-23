import pandas as pd
from tabulate import tabulate

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


def truncate_string(s, max_len, min_len):
    s = str(s)
    if len(s) <= max_len:
        return s + "_" * (min_len - len(s)) 
    return s[:max_len-3] + "..."  

def print_table(df, title=None, sum=None, max_col_widths=None):
    if title:
        print(f"\n{title}\n")

    if sum:
        sum_row = pd.DataFrame([sum], index=["Summary"])
        df = pd.concat([df, sum_row]).iloc[:-1]

    if max_col_widths:
        for col in df.columns:
            max_len = max_col_widths[col]['max']
            min_len = max_col_widths[col]['min']
            if max_len and min_len:
                df[col] = df[col].apply(lambda x: truncate_string(x, max_len, min_len))
    table = tabulate(df, headers='keys', tablefmt='rounded_outline', showindex=False)
    table = "\n".join([" " * 5 + line for line in table.split("\n")])
    print(table)


def print_sub_table(df, title=None, sum=None, max_col_widths=None):
    if title:
        if df['Category'].str.contains("-").any():
            print(f"\n                 {title}\n")
        else:
            print(f"\n   {title}\n")

    if sum:
        sum_row = pd.DataFrame([sum], index=["Summary"])
        df = pd.concat([df, sum_row]).iloc[:-1]

    if max_col_widths:
        for col in df.columns:
            max_len = max_col_widths[col]['max']
            min_len = max_col_widths[col]['min']
            if max_len and min_len:
                df[col] = df[col].apply(lambda x: truncate_string(x, max_len, min_len))
    table = tabulate(df, headers='keys', tablefmt='rounded_outline', showindex=False)
    if df['Category'].str.contains("-").any():
        table = "\n".join(["    " * 4 + line for line in table.split("\n")])
    else: 
        table = "\n".join([" " * 5 + line for line in table.split("\n")])
    print(table)

