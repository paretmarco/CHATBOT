import requests
import json
import os
import subprocess

def send_query_to_chatbot(query):
    chatbot_url = "http://127.0.0.1:5001/api/chatbot"
    data = {
        "user_input": query,
        "max_tokens": 300,
        "additional_context": ""
    }
    response = requests.post(chatbot_url, json=data)
    if response.status_code == 200:
        json_data = response.json()
        if 'response' in json_data:
            print(f"Chatbot response received.")
            print(f"Chatbot response: {json_data['response']}")  # Added line to print the chatbot response
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
    print(f"Input file: {input_file}")

    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    with open(input_file, "r") as infile:
        book_data = json.load(infile)

        for index, record in enumerate(book_data):
            query = record.get("chapter", "").strip()
            print(f"Extracted chapter: '{query}'")
            
            if query:
                print(f"Processing query: {query}")

                chatbot_response = send_query_to_chatbot(f"Complete the concepts of this text with 60 words with an example: '{query}' after the example write A) an exercise to do divided step by step in no more than 70 words B) a witty conclusion C) write with conversational style D) use sometimes the first person")

                if chatbot_response:
                    record["results"] = {
                        "chatbot_response": chatbot_response
                    }
                
                # Save the progress to the JSON file
                with open(input_file, "w") as outfile:
                    json.dump(book_data, outfile, ensure_ascii=False, indent=2)

                print(f"JSON file updated with results for query {index + 1}.")

    print(f"Finished processing queries.")

if __name__ == "__main__":
    process_queries()

subprocess.run(["python", "book_compiler.py"])