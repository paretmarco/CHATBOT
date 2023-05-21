# query_processor.py

import requests
import json
import os
from create_custom_prompt import create_custom_prompt

# [Other code unchanged]

def process_queries():
    input_file = os.path.join("book_created", "book_data.json")  # Input file path
    output_file = os.path.join("book_created", "book.txt")  # Output file path
    print(f"Input file: {input_file}")

    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    with open(input_file, "r") as infile:
        book_data = json.load(infile)  # Load book data

        for index, record in enumerate(book_data):
            query = record.get("chapter", "").strip()
            print(f"Extracted chapter: '{query}'")
            
            if query:
                print(f"Processing query: {query}")

                # Send the query to the chatbot and get the response
                chatbot_response = send_query_to_chatbot(query, draft_summary)

                if chatbot_response:
                    # Update the Google Sheet with the chatbot response in column D
                    write_data_to_sheet(sheet_id, f"D{index + 1}", [[chatbot_response]])
                else:
                    print(f"Error: No chatbot response for query '{query}'.")

            else:
                print("Query is empty. Skipping.")

if __name__ == "__main__":
    process_queries()

