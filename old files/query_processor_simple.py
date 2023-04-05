import requests
import json
import sys
import os
import subprocess

def send_query_to_chatbot(query):
    chatbot_url = "http://127.0.0.1:5001/api/chatbot"
    data = {
        "user_input": query,
        "max_tokens": 100,
        "additional_context": ""
    }
    response = requests.post(chatbot_url, json=data)
    if response.status_code == 200:
        print(f"Chatbot response received.")
        return response.json()["response"]
    else:
        print(f"Error in chatbot response: {response.status_code}")
        return None

def send_query_to_search_snippets(query):
    search_url = "http://127.0.0.1:5000/api/search"
    data = {
        "query": query,
        "num_results": 1
    }
    response = requests.post(search_url, json=data)
    if response.status_code == 200:
        print(f"Search snippet response received.")
        return response.json()["response"]
    else:
        print(f"Error in search snippet response: {response.status_code}")
        return None

def sanitize_filename(filename):
    invalid_chars = {'/', '\\', ':', '*', '?', '<', '>', '|'}
    sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in filename)
    return sanitized_name


def process_queries(input_directory, project_output_directory):
    input_file = os.path.join(input_directory, "input_queries.txt")
    print(f"Input file: {input_file}")

    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    with open(input_file, "r", newline='') as infile:
        for line in infile:
            query = line.strip()
            print(f"Extracted line: '{query}'")
            if query:
                print(f"Processing query: {query}")

                chatbot_response = send_query_to_chatbot(query)
                search_snippet_response = send_query_to_search_snippets(query)

                if chatbot_response or search_snippet_response:
                    output_filename = sanitize_filename(f"{query}.txt")
                    output_path = os.path.join(project_output_directory, output_filename)

                    # Create the project output directory if it doesn't exist
                    os.makedirs(project_output_directory, exist_ok=True)

                    with open(output_path, "w") as outfile:
                        outfile.write(f"Query: {query}\n")
                        outfile.write(f"Chatbot response: {chatbot_response}\n")
                        outfile.write(f"Search snippet response: {search_snippet_response}\n")

    print(f"Finished processing queries. Results saved in '{project_output_directory}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python query_processor.py <input_directory> <output_directory>")
    else:
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]
        process_queries(input_directory, output_directory)

subprocess.run(["python", "book_compiler.py", output_directory])