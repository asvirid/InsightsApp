import os
import pandas as pd
import glob 
from tabulate import tabulate


max_col_widths = {
    'Transaction Date': 10,
    'Category': 20,
    'Debit': 15,
    'Description': 35,
    'Card No.': 7
}

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

    

def read_files(dir):
    dataframes = []
    csv_files = glob.glob(os.path.join(dir, "*.csv")) + glob.glob(os.path.join(dir, "*.CSV"))

    column_mapping = {
        'Date':'Date',
        'Transaction Date': 'Date',
        'Post Date': 'Posted on',
        'Posted Date': 'Posted on',
        'Amount': 'Debit',
        'Debit': 'Debit'
        # Add more mappings as needed
    }
    excluded_cols = ['Memo']

    for filepath in csv_files:
        try: 
            df = pd.read_csv(filepath)
            df = df.drop(columns=excluded_cols, errors ='ignore')
            df.rename(columns=column_mapping, inplace=True)
            if 'Date' in df.columns:
                df['Date'] = parse_dates(df['Date'])
            dataframes.append(df)

        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return dataframes

def truncate_string(s, max_len):
    s = str(s)
    return s.ljust(30) if len(s) <= max_len else s[:max_len-3] + '...'

def print_table(df, title=None, sum=None, max_width=None):
    if title:
        print(f"\n{title}\n")

    if sum:
        sum_row = pd.DataFrame([sum], index=["Summary"])
        df = pd.concat([df, sum_row])

    if max_width:
        for col in df.columns:
            max_len=max_width.get(col)
            if max_len:
                df[col] = df[col].apply(lambda x: truncate_string(str(x), max_len))
    print(tabulate(df, headers='keys', tablefmt='rounded_outline', showindex=False))

def group_and_summarize(df, group_by_col, sum_col):
    grouped = df.groupby(group_by_col)[sum_col].sum().reset_index().sort_values(by='Debit', ascending = False)
    
    grouped_entries = df.groupby(group_by_col)
    return grouped, grouped_entries


def main():
    print("i am working!")
    dir = input("Where are your bank statements csvs? (provide the filepath in the format of /Users/user/Path/toYour/folder without "")\n")
    csv_files = read_files(dir)

    if csv_files:
        combined_df = pd.concat(csv_files, ignore_index=True)
        filtered = combined_df.dropna(subset=["Debit"])
        filtered = filtered[filtered['Type'] != 'Payment']
        filtered = filtered[filtered['Description'] != 'MOBILE PAYMENT - THANK YOU']
        
        sorted = filtered.drop(columns=['Type', 'Credit', 'Posted on'], errors ='ignore')
        if 'Debit' in sorted.columns:
            sorted['Debit'] = sorted['Debit'].abs().round(2) 
        
        sorted['Category'] = sorted['Category'].fillna('Uncategorized')
        
        '''for row in sorted['Category']:
            if sorted['Category'][row] == 'Uncategorized':
                sorted.replace('Uncategorized','Other Travel')'''
            
        grouped_sum, grouped_entries = group_and_summarize(sorted, 'Category', 'Debit')
        print_table(grouped_sum, title="Grouped Summary by Category", max_width=max_col_widths)

        for cat, group_df in grouped_entries:
            cat_sum = group_df['Debit'].sum().round(2)
            summary_stats = {'Debit': f"Sum: {cat_sum}"}
            print_table(group_df,title=f"Entries for Category: {cat}", sum=summary_stats, max_width=max_col_widths)

        sorted = sorted.sort_values(by='Debit', ascending = False)
        spent = sorted['Debit'].sum()
        print_table(sorted)
        print(len(sorted))
        print(f"Total spend this month: {spent}")
            
    else: 
        print("No CSV files were found/all files couldn't be read.")





if __name__ == "__main__":
    main()