import re  # Importing the re library for regular expressions
import csv  # Importing the csv library for CSV file handling

import pdfplumber  # Importing the pdfplumber library for PDF extraction


# Path to the PDF file
pdf_path = '/Users/joathcarrera/Desktop/CSE115A/Soccer-Match-Predictor/2425_Calendars/Bundesliga_Calendar.pdf'

# Path to the output CSV file
base_csv_path = '/Users/joathcarrera/Desktop/CSE115A/Soccer-Match-Predictor/2425_Calendars/Matchday_Calendars/bundesliga_2024-2025fixtures.csv'



def extract_tables_from_pdf(pdf_path):
    
    """
    Extracts all tables from each page of a PDF.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        list: A list of tables extracted from the PDF.
    """
     
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        # Iterate over each page in the PDF
        for page_num, page in enumerate(pdf.pages):
    
            # Extract tables from the current page
            page_tables = page.extract_tables()
    
            # Append the extracted tables to the list
            for table in page_tables:
                tables.append(table)
    return tables



def clean_date(text):

    """
    Reformat different date variants into mm/dd/yyyy.

    Args:
        text: The date text to be cleaned.

    Returns:
        str: The reformatted date string.
    """

    # Possible date formats    
    date_range_pattern = r'(\d{2})\.(\d{2})\.-(\d{2})\.(\d{2})\.(\d{4})'   # Example case: 31.05.-01.06.2024 = 05/31/2024 - 06/01/2024
    date_range_slash_pattern = r'(\d{2})\./(\d{2})\.(\d{2})\.(\d{4})'      # Example case: 30./31.05.2024 = 05/31/2024 - 06/01/2024
    date_range_hyphen_pattern = r'(\d{2})\.-(\d{2})\.(\d{2})\.(\d{4})'     # Example case: 30.-31.05.2024 = 05/31/2024 - 06/01/2024
    single_date_pattern = r'(\d{2})\.(\d{2})\.(\d{4})'                     # Example case: 30.05.2024 = 05/30/2024

    
    # Case 1: format dd.mm.-dd.mm.yyyy
    if (match := re.match(date_range_pattern, text)):  
       
        # Extract start and end dates
        start_day, start_month, end_day, end_month, year = match.groups()
        
        # Reformat start and end dates
        start_date = f"{start_month}/{start_day}/{year}"  
        end_date = f"{end_month}/{end_day}/{year}"  
        
        return f"{start_date} - {end_date}"

    # Case 2: format dd./mm.dd.yyyy   
    elif (match := re.match(date_range_slash_pattern, text)): 
        
        # Extract start and end dates
        start_day, end_day, month, year = match.groups()
        
        # Reformat start and end dates
        start_date = f"{month}/{start_day}/{year}" 
        end_date = f"{month}/{end_day}/{year}" 
        
        return f"{start_date} - {end_date}"

    # Case 3: format dd.-mm.dd.yyyy
    elif (match := re.match(date_range_hyphen_pattern, text)):  
        
        # Extract start and end dates
        start_day, end_day, month, year = match.groups()

        # Reformat start and end dates
        start_date = f"{month}/{start_day}/{year}"  
        end_date = f"{month}/{end_day}/{year}" 

        return f"{start_date} - {end_date}"


    # Case 4: format dd.mm.yyyy
    elif (match := re.match(single_date_pattern, text)):

        # Extract the date 
        day, month, year = match.groups()

        # Reformat date
        date = f"{month}/{day}/{year}"  

        return date

    else:
        return text
    

def clean_and_split_tables(tables):

    """
    Clean data from extracted tables and split them by matchday.

    Args:
        tables: A list of tables extracted from the PDF.

    Returns:
        dict: A dictionary where keys are matchdays and values are lists of cleaned rows.
    """

    # Dictionary to store matchday tables
    tables_by_matchday = {}

    # Iterate over each table
    for table in tables:

        # Iterate over each row in the current table
        for row in table:

            # Row should have at least two columns (Date and Time Columns)
            if row and len(row) > 1:

                # Reformat the dates
                cleaned_row = [clean_date(cell) if cell else cell for cell in row]
                
                # Third column represents the matchday
                if cleaned_row[2] and re.match(r"\d+", cleaned_row[2]):

                    # Single digit matchdays should have a 0 before them
                    matchday = cleaned_row[2].zfill(2)

                    # If matchday is not already in the dictionary, create an empty list for it
                    if matchday not in tables_by_matchday:
                        tables_by_matchday[matchday] = []

                    # Append cleaned row to the list of rows for current matchday    
                    tables_by_matchday[matchday].append(cleaned_row)

     # Each matchday now has its own table.               
    return tables_by_matchday


def filter_bundesliga_matches(matchday_tables):    

    """
    Filter out non-Bundesliga matches from the matchday tables.

    Args:
        matchday_tables: A dictionary where keys are matchdays and values are lists of match rows.

    Returns:
        dict: A dictionary with only Bundesliga matches.
    """
    
    # Create an empty dictionary to store the filtered tables
    filtered_tables = {}
    
    # Define the set of keywords to exclude from the matches
    exclude_keywords = {"DFB", "DFL", "UECL", "A", "UCL", "UEL", "REL"}
    
    # Iterate over each table in the input dictionary
    for matchday, table in matchday_tables.items():
        
        # Create an empty list to store the filtered rows for the current matchday
        filtered_table = []
        
        # Iterate over each row in the current table
        for row in table:
            
            # Check if the row has more than three elements and the fifth element is not empty
            if len(row) > 3 and row[4]:
                
                # Convert the fifth element to lowercase and replace any whitespace with a single space
                lower_case_row = re.sub(r'\s+', ' ', row[4]).lower()
                
                # Check if any of the exclude_keywords are in the lowercase row
                if not any(keyword in lower_case_row for keyword in exclude_keywords):
                    
                    # If no keywords are found, add the row to the filtered_table list
                    filtered_table.append(row)
        
        # If the filtered_table list is not empty, add it to the filtered_tables dictionary
        if filtered_table:
            filtered_tables[matchday] = filtered_table
    
    # Return the filtered_tables dictionary
    return filtered_tables


def save_matchday_tables_to_csv(matchday_tables, base_csv_path):
   
    """
    Save matchday tables to CSV files.

    Args:
        matchday_tables: A dictionary where keys are matchdays and values are lists of match rows.
        csv_base_path (str): The base path for the CSV files.

    """
    
   # Iterate over each matchday and table in the matchday_tables dictionary
    for matchday, table in sorted(matchday_tables.items()):
        
        # Generate a CSV file path for the current matchday and base path
        csv_path = f"{base_csv_path}_matchday_{matchday}.csv"

        # Open the CSV file in write mode with UTF-8 encoding
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row to the CSV file
            writer.writerow(["Date", "Matchday", "Home Team", "Away Team"])

            # Iterate over each row in the current table
            for row in table:
        
                # Check if the row has at least five elements and is not the header row
                if len(row) >= 5 and row != ["Datum", "Spieltag", "Heim", "Gast"]:
        
                    # Write the row data to the CSV file
                    writer.writerow([row[0], row[2], row[4], row[5]])



# Extract tables from the PDF
tables = extract_tables_from_pdf(pdf_path)

# Clean and split the tables into matchday tables
matchday_tables = clean_and_split_tables(tables)

# Filter the matchday tables to include only Bundesliga matches
filtered_matchday_tables = filter_bundesliga_matches(matchday_tables)

# Save the filtered matchday tables to CSV files
save_matchday_tables_to_csv(filtered_matchday_tables, base_csv_path)

