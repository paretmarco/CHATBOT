import openai
import json
import csv
import os
import time
from config import OPENAI_API_KEY
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up API key and model
openai.api_key = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"

# Function to generate a chapter
def generate_chapter(prompt, retries=3, delay=5):
    answers = []
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=prompt,
                temperature=0.7,
                max_tokens=1500,
                stop="\n\n",
            )
            content = response['choices'][0]['message']['content'].strip()

            # Log the user prompt and the received answer
            logging.info(f"User prompt sent: {prompt[-1]['content']}")
            logging.info(f"Answer received: {content}")

            answers.append(content)
            break
        except Exception as e:
            logging.warning(f"Error during API call: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Skipping this answer.")
                answers.append("Error: Unable to generate chapter content.")
                break

    return answers

# Read the draft_text.txt file
with open("drafts/draft_text.txt", "r", encoding="utf-8") as f:
    draft_text = f.read().strip()

# Read the queries.json file
with open("queries.json", "r") as f:
    query_data = json.load(f)

# Initialize the JSON and CSV data structures
json_data = []
csv_data = [["title", "chapter"]]

# Create the output directory if it doesn't exist
output_directory = "book_created"
os.makedirs(output_directory, exist_ok=True)

# Create a comprehensive text file for all chapters
with open(os.path.join(output_directory, "book.txt"), "w") as book_file:
    # Iterate through the query_data and generate chapters
    for data in query_data:
        line = data["line"]
        answers = []
        prompt_base = [
            {"role": "system", "content": "You are an absolute expert in this discipline and you prepare a book. You write sentences full of meanings and crafted with a lot of images."},
            {"role": "assistant", "content": draft_text},
        ]
        for custom_text in data["custom_texts"]:
            prompt = prompt_base + [{"role": "user", "content": custom_text}]
            answers.extend(generate_chapter(prompt))

        # Write the chapters to the comprehensive book file
        book_file.write(f"# {line}\n")
        for idx, answer in enumerate(answers):
            book_file.write(f"## Answer {idx + 1}\n")
            book_file.write(answer)
            book_file.write("\n\n")

        # Append the chapter answers to the JSON and CSV data structures
        json_data.append({"title": line, "answers": answers})
        for answer in answers:
            csv_data.append([line, answer])

        logging.info(f'Generated chapters: {line}')

# Write the JSON and CSV files
with open(os.path.join(output_directory, "book_data.json"), "w") as f:
    json.dump(json_data, f)

with open(os.path.join(output_directory, "book_data.csv"), "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)
