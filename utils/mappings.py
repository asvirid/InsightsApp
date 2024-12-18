from utils.constants import * 
max_col_widths = {
    'Transaction Date': {'min': 2, 'max': 3},
    'Category': {'min': 15, 'max': 37},
    'Debit': {'min': 5, 'max': 15},
    'Description': {'min': 24, 'max': 24},
    'Card No.': {'min': 4, 'max': 8},
    'Date': {'min': 10, 'max': 10}
}

#add keywords from the description column to associate with some specific category
keyword_to_category = {
    'Coffee': ['cafe', 'forge', 'caffe', 'coffee', 'rustica', 'starbucks', 'dunkin', 'tatte'],
    'Transportation': ['Uber', 'uber', 'UBER', 'bus', 'lyft','mbta', 'tripshot', 'rail', 'parking'],
    'Dining': ['restaurant', 'diner', 'life aliv', 'bagel', 'doorda', 'chipotle', 'dine', 'yvonne', 'widowmaker', 'andbrighton', 'cava', 'inflight', 
               'howl', 'el jefes', 'pho n'],
    'Dining - travel': ['amtrak'],
    'Groceries': ['market', 'target', 'bonus', 'whole foods', 'trader joe'],
    'Groceries - snacks': ['cambridge nat'],
    'Groceries - pharma/cvs': ['cvs'],
    'Shopping': ['papersource'],
    'Shopping - amazon': ['amazon', 'amzn'],
    'Shopping - cosmetics': ['sephora', 'lush'],
    'Shopping - clothes': ['aritzia', 'lululemon', 'alo-yoga', 'uniqlo', 'anthropologie', 'sunglass', 'cos'],
    'Shopping - gifts': ['nuts factory', 'zion outfitter', 'le macaron cacambridge'],
    'Shopping - temu':['temu'],
    'Shopping - Gear': ['arcteryx', 'backcountry', 'rei', 'nike'],
    'Shopping - bookshops': ['coop', 'books'], 
    'Travel/Flights':['explorer', 'american', 'gulf', 'yarts', 'yosemite', 'fresno', 'airport', 'phoenix'],
    'Healthcare': ['orthodontics', 'asthma ctr'],
    'Alco': ['seven hills'], 
    'Subscriptions': ['fitrec', 'down under', 'babbel', 'spotify', 'adobe', 'apple', 'peacock', 'amazon prime', 'renewal membership fee', 'magic util', 'calm.com'],
    'Therapy':['smartglocal'],
    'Taxes':['intuit'],
    'Personal':['best nails', 'alexander safa'],
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