import json
import re
from google_sheets_helper import read_data_from_sheet, find_sheet_by_title

# Read the config file
with open('config.json') as config_file:
    config = json.load(config_file)
    sheet_name = config['sheet_name']  # Read the sheet_name from the config file

# Find the Google Sheet with the specified name
folder_id = "1O4__jxbTubCObzCCn08oPe0bc0DlP-uO"  # Replace with the folder ID of the "AI_CREATED_BOOKS" directory
sheet_id = find_sheet_by_title(sheet_name, folder_id)

read_range = "A2:J"  # Define the range for reading data
sheet_data = read_data_from_sheet(sheet_id, read_range)

output_file_path = "C:\\D\\documenti\\AI\\program24\\book_created\\combined_output.txt"
with open(output_file_path, "w", encoding='utf-8') as output_file:
    for index, record in enumerate(sheet_data):
        chapter_title = record[1] if len(record) > 1 else "INFO TO COMPLETE"
        chapter_content = record[2] if len(record) > 2 else "INFO TO COMPLETE"
        chatbot_response = record[3] if len(record) > 3 else "INFO TO COMPLETE"
        slogan = record[4] if len(record) > 4 else "INFO TO COMPLETE"
        chatbot_response_completion = record[5] if len(record) > 5 else "INFO TO COMPLETE"
        column_F_content = record[6] if len(record) > 6 else "INFO TO COMPLETE"  # Read column F content
        column_G_content = record[7] if len(record) > 7 else "INFO TO COMPLETE"
        column_I_content = record[8] if len(record) > 8 else "INFO TO COMPLETE"
        column_J_content = record[9] if len(record) > 9 else "INFO TO COMPLETE"

        if re.match(r'^\d+\.\d+', chapter_title):
            output_file.write(f"## {chapter_title} ##\n")
        else:
            output_file.write(f"# {chapter_title} #\n")
        output_file.write(f"# {slogan}\n")
        output_file.write("\n")
        output_file.write(f"{chapter_content}\n")
        output_file.write("# \n")
        output_file.write(f"{chatbot_response}\n")
        output_file.write("# \n")
        output_file.write(f"{chatbot_response_completion}\n")
        output_file.write("# \n")
        output_file.write(f"{column_I_content}\n")
        output_file.write("# \n")
        output_file.write(f"{column_J_content}\n")
        output_file.write("# Conclusioni\n")
        output_file.write(f"{column_F_content}\n")  # Write the content of column F
        output_file.write("\n\n\n# \n#\n\n")

