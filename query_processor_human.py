# BOOK PROCESSING to continue processing and smoothing text
import json
import logging
import os
from chatbot import process_chatbot_request

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load input chunks from a JSON file
def load_input_chunks(input_file):
    with open(input_file, "r", encoding='utf-8') as infile:
        return json.load(infile)

# Write output chunks in a .txt file
def write_output_chunk(chunk, response, output_file):
    with open(output_file, "a", encoding='utf-8') as outfile:
        outfile.write(response)
        outfile.write("\n\n")

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

input_file = config["json_file"]
output_file = config["input_file"]
additional_context = config["additional_context"]
author_personality = config['author_personality']
max_tokens = config['max_tokens']
model = config['model']
user_id = config['user_id']
temperature = config['temperature']
frequency_penalty = config['frequency_penalty']
language = config['language']

# Reinitialize the output file
with open(output_file, "w", encoding='utf-8') as outfile:
    pass

# Load chunks from input file
chunks = load_input_chunks(input_file)

#  lines starting with # are written to the output file but not processed, and lines starting with #TITLE are neither written nor processed.
last_chunk = None
for chunk in chunks:
    if chunk.startswith("#TITLE") or not chunk.strip():  # Skip only lines with #TITLE and blank lines
        continue  # Add this line to skip processing the current chunk
    elif chunk.startswith("#"):  # If the line starts with #
        write_output_chunk(chunk, chunk, output_file)  # Write it to the output file
        continue  # Skip processing the current chunk
    else:
        if last_chunk and last_chunk.startswith("#") and not last_chunk.strip():
            user_input = f'Continua "{last_chunk}" utilizzando questo testo (###{chunk}###) ed aggiungendo spunti interessanti'
        else:
            user_input = f"Please write in this language: '''{language} ''' and Increase NLP Perlexity and Burstiness in a random way for each phrase in order it seems written by a human: ###{chunk}### and if possible add also a metaphor to the text."
        
        # Send the request to the chatbot and get the response
        response = process_chatbot_request(user_input, max_tokens, author_personality, additional_context, model, user_id, temperature, frequency_penalty)
        write_output_chunk(chunk, response, output_file)

    last_chunk = chunk

# Log completion of the task
logging.info(f"Task completed: Paraphrased chunks are saved in '{output_file}'")
