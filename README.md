## Insights App
Insights App is a python app to show a summary and categorization of your bank transactions across multiple bank CSVs (assuming downloaded to your PC). 
Supported banks: AMEX, Capital One, Chase.


## To run:
1. Download all your bank statements in .csv format into a folder of your choice
2. Execute the following from the terminal from inside this app directory:
    `python3 insights.py <yourFolderwithStatements>`

### Additional configurations:
If you would like to personalize your categories, you can edit keywords in `keyword_to_category` object in `mappings.py` file. When you add a keyword to the list, the app will pick up the ehtry containing this keyword and put it into the desired category of your choice.  