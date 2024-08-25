max_col_widths = {
    'Transaction Date': {'min': 2, 'max': 3},
    'Category': {'min': 44, 'max': 45},
    'Debit': {'min': 5, 'max': 15},
    'Description': {'min': 9, 'max': 30},
    'Card No.': {'min': 5, 'max': 7}
}

#add keywords from the description column to associate with some specific category
keyword_to_category = {
    'Coffee': ['cafe', 'forge', 'caffe', 'coffee', 'rustica', 'starbucks', 'dunkin', 'tatte'],
    'Transportation': ['Uber', 'uber', 'UBER', 'bus', 'lyft','mbta', 'tripshot', 'rail', 'parking'],
    'Dining Out': ['restaurant', 'diner', 'life aliv', 'bagel', 'doorda', 'chipotle', 'dine', 'yvonne', 'widowmaker', 'andbrighton'],
    'Groceries': ['market', 'target', 'bonus', 'cambridge nat', 'whole foods', 'cvs', 'trader joe'],
    'Shopping - amazon': ['amazon', 'amzn'],
    'Shopping - cosmetics': ['sephora'],
    'Shopping - clothes': ['aritzia', 'lululemon', 'alo-yoga', 'uniqlo'],
    'Travel/Flights':['explorer', 'american', 'gulf', 'yarts', 'yosemite', 'fresno', 'airport', 'phoenix'],
    'Health & Wellness': ['orthodontics'],
    'Gear': ['arcteryx', 'backcountry'],
    'Alco': ['seven hills'], 
    'Subscriptions': ['fitrec', 'down under', 'babbel', 'spotify', 'adobe', 'apple', 'peacock', 'amazon prime', 'renewal membership fee'],
    'Therapy':['smartglocal'],
    'Taxes':['intuit'],
    'Maintenance/Repairs': ['bicycle belle']
}

cards = {
    'transaction_download': 'cap1',
    '8976': 'cap1Silver',
    '0052':'reserve',
    '6007':'freedom',
    'activity': 'amex'
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