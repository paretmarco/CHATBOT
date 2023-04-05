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

            return content
        except Exception as e:
            logging.warning(f"Error during API call: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Skipping this chapter.")
                return "Error: Unable to generate chapter content."

# Read the draft_text.txt file
with open("drafts/draft_text.txt", "r", encoding="utf-8") as f:
    draft_text = f.read().strip()

# Function to generate a summary
def generate_summary(text, retries=3, delay=5):
    summary_prompt = [
        {"role": "system", "content": "You are a highly skilled summarizer. Summarize the following text:"},
        {"role": "assistant", "content": text},
        {"role": "user", "content": "Please provide a summary of the main points in no more than 600 tokens."},
    ]

    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=summary_prompt,
                temperature=0.7,
                max_tokens=100,
                stop=None,
            )
            summary = response['choices'][0]['message']['content'].strip()
            
            # Log the user prompt and the received answer
            logging.info(f"User prompt sent: {summary_prompt[-1]['content']}")
            logging.info(f"Summary received: {summary}")

            return summary
        except Exception as e:
            logging.warning(f"Error during API call: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Skipping summary generation.")
                return "Error: Unable to generate summary."

# Generate a summary of the draft_text
draft_summary = generate_summary(draft_text)

# Read the input_queries.txt file and remove empty lines
with open("input/input_queries.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]
    logging.info(f"Read {len(lines)} lines from input_queries.txt")

# Initialize the JSON and CSV data structures
json_data = []
csv_data = [["title", "chapter"]]

# Create the output directory if it doesn't exist
output_directory = "book_created"
os.makedirs(output_directory, exist_ok=True)

# Create a comprehensive text file for all chapters
with open(os.path.join(output_directory, "book.txt"), "w") as book_file:
    # Iterate through the lines and generate chapters
    for line in lines:
        line = line.strip()
        prompt = [
            {"role": "system", "content": "You are an absolute expert in this discipline and you prepare a book. You write sentences full of meanings and crafted with a lot of images."},
            {"role": "assistant", "content": draft_text},
            {"role": "user", "content": f"Continue {draft_summary} developing in a clear way the specific concept for this chapter {line}. You are the author and you write in the first person most of the times. Please write a detailed text of at least 55 words simple to understand even for a 15 years old, after and provide after in a new paragraph 40 words to what purpose it can be useful, and at the end an example of at least 60 words."},
        ]
        chapter = generate_chapter(prompt)

        # Write the chapter to a text file
        filename = line.replace('"', '') + ".txt"
        # Removed lines here for writing individual files

        # Write the chapter to the comprehensive book file
        book_file.write(f"# {line}\n")
        book_file.write(chapter)
        book_file.write("\n\n")

        # Append the chapter to the JSON and CSV data structures
        json_data.append({"title": line, "chapter": chapter})
        csv_data.append([line, chapter])

        logging.info(f'Generated chapter: {line}')

# Write the JSON and CSV files
with open(os.path.join(output_directory, "book_data.json"), "w") as f:
    json.dump(json_data, f)

with open(os.path.join(output_directory, "book_data.csv"), "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

