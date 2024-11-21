import pandas as pd
import sys
from utils.constants import * 
from utils.utils import *
from tabulate import tabulate
from utils.mappings import max_col_widths, keyword_to_category
from reader.file_reader import read_files

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
        if current_category == 'Food & Drink':
            return 'Dining'
        else:
            return current_category
    
    return 'Uncategorized'

def update_uncategorized_entries(df, keyword_to_category):
    df['Category'] = df.apply(lambda row: assign_category(row, keyword_to_category), axis=1)
    return df

def group_and_summarize(df, group_by_col, sum_col, sum_cat_month):
    grouped = df.groupby(group_by_col)[sum_col].sum().reset_index().sort_values(by='Debit', ascending = False).round(2)
    
    grouped_entries = df.groupby(group_by_col)
    grouped_by_month = df.groupby(sum_cat_month)
    return grouped, grouped_entries, grouped_by_month

def print_summary_report(total_sum, cat, amt, month):
        summaryReport = f"{TEAL_BLUE}Summary Report{RESET}" + "\n--------------" + f"\nYou spent ${total_sum.get('sum').round(2)} this {month}\nYour largest purchase was ${total_sum.get('max')}\nYou made {total_sum.get('count')} purchases in total this month"
        print(f"{ summaryReport }")
        print(f"Your largest Spending Category was '{cat}' (${amt:.2f})\n")

def print_categories(grouped_entries):
    for cat, group_df in grouped_entries:
            cat_sum = group_df['Debit'].sum().round(2)
            summary_stats = {'Debit': f"::{cat_sum}"}
            print_table(group_df,title=f"{cat}: ${cat_sum}", sum=summary_stats, max_col_widths=max_col_widths)

def print_total_summary(sorted, spent):
    print(f"Total spent: ${spent}")
    print_table(sorted.sort_values(by='Category', ascending = True))

def main(path, monthInput):
    dir = path + monthInput
    csv_files = read_files(dir)

    if csv_files.notnull:
        #populate the card number column 
        combined_df = csv_files
        filtered = combined_df.dropna(subset=["Debit"])
        if 'Type' in filtered.columns:
            filtered = filtered[(filtered['Type'] != 'Payment') & (filtered['Type'] != 'Return')]
        filtered = filtered[(filtered['Description'] != 'MOBILE PAYMENT - THANK YOU') & 
                            (filtered['Description'] != 'TRAVEL CREDIT $300/YEAR')&
                            (filtered['Description'] != 'Returned Mobile ACH Payme')& 
                            (filtered['Description'] != 'AMEX Dining Credit')]
    
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
        
    
        grouped_sum, grouped_entries, cat_month = group_and_summarize(sorted, 'Category', 'Debit', "Date")

        print_categories(grouped_entries)

        sorted = sorted.sort_values(by='Debit', ascending = False).round(2)
        spent = sorted['Debit'].sum().round(2)
        print_total_summary(sorted, spent)
        
        #print_table(sorted.sort_values(by='Date', ascending = True))
        print(len(sorted))

         # Print the summary
        print_summary_report(total_sum, largest_spending_category, largest_spending_amount, monthInput)

        print_table(grouped_sum, max_col_widths=max_col_widths)    
        #print_table(cat_month, max_col_widths=max_col_widths)    
            
    else: 
        print("No CSV files were found/all files couldn't be read.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide a folder name with statements you would like to analyze.")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])