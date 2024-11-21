## Insights App
Insights App is a python app to show a summary and categorization of your bank transactions across multiple bank CSVs (assuming downloaded to your PC). 

### Supported Banks
- AMEX
- Capital One
- Chase

## To run:
1. **Prepare Your Statements**  
   Download your bank statements in `.csv` format and save them in a folder.

2. **Run the Script**  
   Navigate to the Insights app directory in your terminal and execute the following command:

   ```bash
   python3 insights.py <path> <folder> 
   ```
   
   `<path>`: Full path to the folder containing your bank statements.
    
   `<folder>`: Name of the folder.

### Additional configurations:
You can customize categories to better organize your insights:

1. Open the `mappings.py` file.
2. Modify the `keyword_to_category` object:
* Add keywords to the lists for any category.
* Transactions containing the specified keywords will automatically be categorized.