# import necessary modules
import json
import os
from google_sheets_helper import read_data_from_sheet

def write_to_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

import logging

def retrieve_and_save_data(sheet_id, range_name):
    logging.info('Reading data from the Google Sheet.')
    
    # Retrieve data from the Google Sheet
    data = read_data_from_sheet(sheet_id, range_name)
    
    # Check if data was retrieved successfully
    if data is None:
        logging.error('No data retrieved from the Google Sheet.')
        return
    
    logging.info(f'Retrieved {len(data)} rows of data from the Google Sheet.')
    
    # Create youtube_uploads directory if it doesn't exist
    os.makedirs("youtube_uploads", exist_ok=True)
    
    # Each row will be written to a separate file
    for i, row in enumerate(data):
        # Check if row has the expected number of columns
        if len(row) < 7:
            logging.warning(f'Row {i} has only {len(row)} columns. Skipping this row.')
            continue
        
        # Extract data from each row
        title = row[1]
        url = row[2]
        description = row[3]
        num_views = row[6]
        
        # Prepare data for JSON file
        file_data = {
            "title": title,
            "url": url,
            "description": description,
            "views": num_views,
        }

        # Define the file path
        file_path = f"youtube_uploads/data_{i}.json"
        
        logging.info(f'Writing data for row {i} to {file_path}.')
        
        # Write the data to a JSON file
        write_to_json_file(file_data, file_path)

    logging.info('Finished writing data to files.')

# Use the function with your specific Google Sheet ID and range
retrieve_and_save_data(sheet_id="1_dQ50_EeFz2X29KiLhEpYl05TzzA1Tx4LcmorCVwG9w", range_name="Sheet1")
