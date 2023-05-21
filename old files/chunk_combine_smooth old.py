import json
import logging
import os

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load output chunks from a JSON file
def load_output_chunks(output_file):
    with open(output_file, "r") as infile:
        return json.load(infile)

# Create the final document using the output chunks
def create_final_document(output_chunks, final_output_file):
    with open(final_output_file, "w", encoding="utf-8") as outfile:
        for chunk, response in output_chunks.items():
            if chunk.startswith("#"):
                outfile.write(response + "\n")  # Use 'response' instead of 'chunk'
            else:
                outfile.write(response + "\n")

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

output_file = config["output_file"]
final_output_file = "book_created/combined_output_smooth.txt"

# Create the directory if it doesn't exist
if not os.path.exists("book_created"):
    os.makedirs("book_created")

output_chunks = load_output_chunks(output_file)
create_final_document(output_chunks, final_output_file)

# Log the location of the result file
logging.info(f"Result file saved as: {final_output_file}")
