import os
import pandas as pd
import glob 
from tabulate import tabulate
from mappings import max_col_widths, keyword_to_category
from file_reader import read_files

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

    if True:
        #populate the card number column 
        combined_df = csv_files
        filtered = combined_df.dropna(subset=["Debit"])
        if 'Type' in filtered.columns:
            filtered = filtered[(filtered['Type'] != 'Payment') & (filtered['Type'] != 'Return')]
        filtered = filtered[(filtered['Description'] != 'MOBILE PAYMENT - THANK YOU') & (filtered['Description'] != 'Returned Mobile ACH Payme')& (filtered['Description'] != 'AMEX Dining Credit')]
    
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
        summaryReport = "\nSummary Report" + "\n--------------" + f"\nYou spent ${total_sum.get('sum').round(2)} this {month}\nYour largest purchase was ${total_sum.get('max')}\nYou made {total_sum.get('count')} purchases in total this month"
        
        

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
        print(f"Your largest Spending Category was '{largest_spending_category}' (${largest_spending_amount:.2f})\n")
        print_table(grouped_sum, max_col_widths=max_col_widths)    
            
    else: 
        print("No CSV files were found/all files couldn't be read.")

if __name__ == "__main__":
    main()