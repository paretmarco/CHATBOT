import requests
import json
import os
from create_custom_prompt import create_custom_prompt
from google_sheets_helper import read_data_from_sheet, find_sheet_by_title, write_data_to_sheet

with open('config.json') as config_file:
    config = json.load(config_file)
    author_personality = config['author_personality']
    max_tokens = config['max_tokens']
    num_results = config['num_results']
    sheet_name = config['sheet_name']  # Read the sheet_name from the config file
    language = config['language']

def load_draft_summary():
    try:
        with open("drafts/draft_summary.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("draft_summary.txt not found.")
        return ""

# Load the draft summary
draft_summary = load_draft_summary()

# Read the book_title.txt file
with open("drafts/book_title.txt", "r", encoding="utf-8") as f:
    book_title = f.read().strip()

# Create the sheet_name with the number of lines and the content of the book_title.txt file
sheet_name = config['sheet_name']
folder_id = "1O4__jxbTubCObzCCn08oPe0bc0DlP-uO"  # Replace with the folder ID of the "AI_CREATED_BOOKS" directory
sheet_id = find_sheet_by_title(sheet_name, folder_id)

# Define the sheet ID and the range for reading data
READ_RANGE = "A2:C"  # Adjust this range based on your sheet's structure
sheet_data = read_data_from_sheet(sheet_id, READ_RANGE)

def send_query_to_chatbot(query, summary):
    chatbot_url = "http://127.0.0.1:5001/api/chatbot"
    data = {
        "user_input": query,
        "max_tokens": 400,
        "additional_context": summary
    }
    response = requests.post(chatbot_url, json=data)  # Send POST request to the chatbot
    if response.status_code == 200:
        json_data = response.json()
        if 'response' in json_data:
            print(f"Chatbot response received.")
            print(f"Chatbot RESPONSE: {json_data['response']}")
            return json_data["response"]
        else:
            print("Error: 'response' key is missing in the chatbot JSON data.")
            return None
    else:
        print(f"Error in chatbot response: {response.status_code}")
        return None

def sanitize_filename(filename):
    invalid_chars = {'/', '\\', ':', '*', '?', '<', '>', '|'}
    sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in filename)  # Replace invalid characters
    return sanitized_name

def process_queries():
    output_file = os.path.join("book_created", "book.txt")  # Output file path

    for index, record in enumerate(sheet_data):
        query = record[2].strip()  # Assuming the query is in column C (index 2)
        print(f"Extracted chapter: '{query}'")

        if query:
            print(f"Processing query: {query}")

            # Send the query to the chatbot and get the response
            chatbot_response = send_query_to_chatbot(f"Speak the following language: {language}. You are writing the paragraph after this one :###{query}###. You must not repeat concepts, and you use no no more than 50 words giving a practical example. After the example write an exercise to do divided step by step in no more than 40 words. Add at the end a curious conclusion 30 words. Important: write with conversational style and many images and use sometimes the first person.", draft_summary)

            if chatbot_response:
                with open(output_file, "a", encoding="utf-8") as outfile:
                    outfile.write(chatbot_response)
                    outfile.write("\n\n")

                # Update the Google Sheet with the chatbot response
                # Assuming the chatbot_response should be written to column D (index 3)
                response_range = f"D{index + 2}"
                write_data_to_sheet(sheet_id, response_range, [[chatbot_response]])

                print(f"Google Sheet updated with results for query {index + 1}.")
            else:
                print(f"Skipping empty query at index {index + 1}.")
    print(f"Finished processing queries.")

if __name__ == "__main__":
    process_queries()
