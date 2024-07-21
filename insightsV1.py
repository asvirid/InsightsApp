import os
import pandas as pd
import glob 
from tabulate import tabulate


max_col_widths = {
    'Transaction Date': {'min': 2, 'max': 3},
    'Category': {'min': 44, 'max': 45},
    'Debit': {'min': 5, 'max': 15},
    'Description': {'min': 9, 'max': 30},
    'Card No.': {'min': 5, 'max': 7}
}

keyword_to_category = {
    'Coffee': ['cafe', 'forge', 'caffe', 'coffee', 'rustica', 'starbucks', 'dunkin'],
    'Transportation': ['Uber', 'uber', 'UBER', 'bus', 'lyft','mbta', 'tripshot'],
    'Dining': ['restaurant', 'diner', 'life aliv', 'bagel', 'doorda', 'chipotle', 'dine'],
    'Groceries': ['market', 'target', 'bonus', 'cambridge nat', 'whole foods', 'cvs', 'trader joe'],
    'Travel':['explorer', 'american', 'gulf'],
    'Gear': ['arcteryx'],
    'Alco': ['seven hills'],
    'Subscriptions': ['fitrec', 'down under', 'babbel', 'spotify', 'adobe', 'apple']
}

cards = {
    'Chase': '1835',
    'Cap1Silver': '8976',
    'AMEX': ''
}

budget = {
    'Merchandise': 100,
    'Health & Wellness': 100,
    'Shopping': 100,
    'Entertainment': 100,
    'Travel': 100,
    'Other Services': 100,
    'Groceries': 100,
    'Other': 100,
    'Food & Drink': 100,
    'Other Travel': 100,
    'Health Care': 100,
    'Education': 100,
    'Dining': 100,
    'Fees & Adjustments': 100,
    'Uncategorized': 100,
}

def summarize_column(df, column_name):
    summary = {
        'sum': df[column_name].sum(),
        'mean': df[column_name].mean(),
        'median': df[column_name].median(),
        'min': df[column_name].min(),
        'max': df[column_name].max(),
        'count': df[column_name].count()
    }
    return summary


def assign_category(row, keyword_to_category):
    description = row['Description']
    current_category = row['Category']
    
    if pd.isnull(description) or description.strip() == '':
        return 'Uncategorized'
    
    description = description.lower()
    for category, keywords in keyword_to_category.items():
        if any(keyword in description for keyword in keywords):
            return category
    if pd.notnull(current_category) and current_category.strip() != '':
        if current_category == 'Merchandise':
            return 'Shopping'
        else:
            return current_category
    
    return 'Uncategorized'

def update_uncategorized_entries(df, keyword_to_category):
    df['Category'] = df.apply(lambda row: assign_category(row, keyword_to_category), axis=1)
    return df

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

def truncate_string(s, max_len, min_len):
    s = str(s)
    return s.ljust(min_len) if len(s) <= max_len else s[:max_len-3] + '...'

def print_table(df, title=None, sum=None, max_col_widths=None):
    if title:
        print(f"\n{title}\n")

    if sum:
        sum_row = pd.DataFrame([sum], index=["Summary"])
        df = pd.concat([df, sum_row])

    if max_col_widths:
        for col in df.columns:
            max_len = max_col_widths.get(col, {}).get('max')
            min_len = max_col_widths.get(col, {}).get('min')
            if max_len and min_len:
                df[col] = df[col].apply(lambda x: truncate_string(x, max_len, min_len))
    print(tabulate(df, headers='keys', tablefmt='rounded_outline', showindex=False))

def group_and_summarize(df, group_by_col, sum_col):
    grouped = df.groupby(group_by_col)[sum_col].sum().reset_index().sort_values(by='Debit', ascending = False).round(2)
    
    grouped_entries = df.groupby(group_by_col)
    return grouped, grouped_entries


def main():
    print("i am working!")
    #dir = input("Where are your bank statements csvs? (provide the filepath in the format of /Users/user/Path/toYour/folder without "")\n")
    month = str(input("Which month do you want to see summary for?(provide the month in lowercase format )\n"))
    dir = "/Users/nafanya/Desktop/statements_insights/" + month
    csv_files = read_files(dir)

    if csv_files:
        combined_df = pd.concat(csv_files, ignore_index=True)
        filtered = combined_df.dropna(subset=["Debit"])
        if filtered.columns.__contains__ == 'Type':
            filtered = filtered[filtered['Type'] != 'Payment']
        filtered = filtered[(filtered['Description'] != 'MOBILE PAYMENT - THANK YOU') & (filtered['Description'] != 'Payment Thank You-Mobile')]
        
        sorted = filtered.drop(columns=['Type', 'Credit', 'Posted on'], errors ='ignore').round(2)
        if 'Debit' in sorted.columns:
            sorted['Debit'] = sorted['Debit'].abs()
        
        # Calculate total sum
    
        sorted = update_uncategorized_entries(sorted, keyword_to_category)
        
        total_sum = summarize_column(sorted, 'Debit')
        print(f"Total Sum of 'Debit' column: {total_sum}")
        category_totals = sorted.groupby('Category')['Debit'].sum().sort_values(ascending=False)
        largest_spending_category = category_totals.idxmax()
        largest_spending_amount = category_totals.max()
        # Print the summary
        summaryReport = "\nSummary Report" + "\n--------------" + f"\nTotal Spending: ${total_sum.get('sum').round(2)}\nLargest Purchase: ${total_sum.get('max')}\nPurchase #: {total_sum.get('count')} "
        
        

        grouped_sum, grouped_entries = group_and_summarize(sorted, 'Category', 'Debit')

        for cat, group_df in grouped_entries:
            cat_sum = group_df['Debit'].sum().round(2)
            summary_stats = {'Debit': f"::{cat_sum}"}
            print_table(group_df,title=f"{cat}: ${cat_sum}", sum=summary_stats, max_col_widths=max_col_widths)

        
    
        sorted = sorted.sort_values(by='Debit', ascending = False).round(2)
        spent = sorted['Debit'].sum().round(2)
        print(f"Total spent: ${spent}")
        print_table(sorted.sort_values(by='Category', ascending = True))
        print(len(sorted))
        print(f"{summaryReport}")
        print(f"Largest Spending Category: {largest_spending_category} (${largest_spending_amount:.2f})\n")
        print_table(grouped_sum, max_col_widths=max_col_widths)
        
            
    else: 
        print("No CSV files were found/all files couldn't be read.")





if __name__ == "__main__":
    main()