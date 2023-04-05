import os
import sys
import json

def sanitize_filename(filename):
    invalid_chars = {'/', '\\', ':', '*', '?', '<', '>', '|'}
    sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in filename)
    return sanitized_name

def create_book(output_directory, book_filename):
    book_path = os.path.join(output_directory, book_filename)
    input_file = os.path.join("book_created", "book_data.json")

    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    with open(input_file, "r") as infile:
        book_data = json.load(infile)

    with open(book_path, "w") as book:
        for record in book_data:
            title = record.get("title", "").strip()
            chapter = record.get("chapter", "").strip()
            results = record.get("results", {})
            chatbot_response = results.get("chatbot_response", "")

            if title and chapter and chatbot_response:
                book.write(f"# {title}\n")
                book.write(f"{chapter}\n")
                book.write(chatbot_response)
                book.write("\n\n")

    print(f"Book created at '{book_path}'.")

if __name__ == "__main__":
    output_directory = "output_book"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    i = 1
    while os.path.exists(os.path.join(output_directory, f"book_{i}.txt")):
        i += 1
    create_book(output_directory, f"book_{i}.txt")
