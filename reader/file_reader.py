import os
import pandas as pd
import glob 
from utils.utils import parse_dates
from utils.mappings import cards

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
            
            filename = os.path.basename(filepath).lower()
            cardname = 'unknown'
            for card in cards:
                if card in filename:
                    cardname = cards[card]
                    break
            df['Card No.'] = cardname
            dataframes.append(df)

        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    final_df = pd.concat(dataframes, ignore_index=True)
    return final_df