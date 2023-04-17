import requests
import json
import os
from create_custom_prompt import create_custom_prompt

def send_query_to_chatbot(query):
    chatbot_url = "http://127.0.0.1:5001/api/chatbot"
    data = {
        "user_input": query,
        "max_tokens": 400,
        "additional_context": ""
    }
    response = requests.post(chatbot_url, json=data)
    if response.status_code == 200:
        json_data = response.json()
        if 'response' in json_data:
            print(f"Chatbot response received.")
            print(f"Chatbot response: {json_data['response']}")
            return json_data["response"]
        else:
            print("Error: 'response' key is missing in the chatbot JSON data.")
            return None
    else:
        print(f"Error in chatbot response: {response.status_code}")
        return None

def sanitize_filename(filename):
    invalid_chars = {'/', '\\', ':', '*', '?', '<', '>', '|'}
    sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in filename)
    return sanitized_name

def process_queries():
    input_file = os.path.join("book_created", "book_data.json")
    output_file = os.path.join("book_created", "book.txt")
    print(f"Input file: {input_file}")

    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    with open(input_file, "r") as infile:
        book_data = json.load(infile)

        for index, record in enumerate(book_data):
            query = record.get("chapter", "").strip()
            print(f"[{index + 1}/{len(book_data)}] Extracted chapter: '{query}'")

            if query:
                print(f"Processing query: {query}")

                previous_chapter = book_data[index - 1]["chapter"] if index > 0 else ""
                custom_prompt = create_custom_prompt(previous_chapter, query, record["chapter"])

                chatbot_response = send_query_to_chatbot(custom_prompt)

                if chatbot_response:
                    record["results"] = {
                        "chatbot_response": chatbot_response
                    }

                    with open(output_file, "a", encoding="utf-8") as outfile:
                        outfile.write(chatbot_response)
                        outfile.write("\n\n")

                with open(input_file, "w") as jsonfile:
                    json.dump(book_data, jsonfile, ensure_ascii=False, indent=2)

                print(f"JSON file updated with results for query {index + 1}.")
            else:
                print(f"Skipping empty query at index {index + 1}.")

    print(f"Finished processing queries.")

if __name__ == "__main__":
    process_queries()
