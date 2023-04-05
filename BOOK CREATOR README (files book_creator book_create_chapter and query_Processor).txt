Book Creator README
This README will guide you through using the Book Creator, a Python script that generates a book based on the input provided. The script uses OpenAI's GPT-3.5-turbo to generate content and a local chatbot to complete the text based on an existing database.

Prerequisites
Python 3.7 or higher
OpenAI Python library
Requests library
You can install the required libraries using the following command:

bash
Copy code
pip install openai requests
Usage
Create a folder named drafts and place a text file named draft_text.txt containing the text of the book inside the folder.

Run book_creator.py. This script generates the book's structure and initial content using OpenAI's GPT-3.5-turbo. The output is saved in a folder named book_created, with each chapter saved as a separate text file. A comprehensive text file named book.txt, containing all chapters, is also created. Metadata for the book is saved in book_data.json and book_data.csv.

Run query_processor.py. This script processes each chapter and completes the text using a local chatbot based on an existing database. The results are saved in the book_data.json file in the book_created folder.

Run book_compiler.py (not provided in the original code). This script should combine the generated content from GPT-3.5-turbo and the local chatbot, and create the final version of the book.

Troubleshooting
Make sure the required libraries are installed.
Ensure the input files (draft_text.txt and input_queries.txt) are in their respective folders.
If you encounter any issues with the API calls, check your API key and make sure it is set correctly in the config.py file.
Notes
The generated book may not be perfect and might require manual editing for better coherence and consistency.
Using GPT-3.5-turbo helps with the structure of the book, but the content might lack a personal touch. The local chatbot helps to improve this aspect by utilizing the existing database of texts.