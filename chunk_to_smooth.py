import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config_file_path = "config.json"

with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

input_file_path = config["input_file"]
output_file_path = "book_created/combined_output.json"

chunks = []
chapter_counter = 1

def is_title(line):
    return line.startswith("#") and line.endswith("#\n") and len(line.strip()) > 1

def is_separator(line):
    return line.strip() == "#"

with open(input_file_path, 'r', encoding='utf-8') as input_file:
    line_buffer = []

    for line in input_file:
        if (is_title(line) or is_separator(line)) and line_buffer:
            chunks.append(" ".join(line_buffer))
            line_buffer = []

        if is_title(line):
            chunks.append(f"#TITLE{chapter_counter}")
            chapter_counter += 1
            chunks.append(line.strip("#\n"))
        elif is_separator(line):
            chunks.append("#")
            chunks.append(" ".join(line_buffer))
            line_buffer = []
        else:
            line_buffer.append(line.strip())

    if line_buffer:
        chunks.append(" ".join(line_buffer))

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(chunks, output_file)

logging.info(f'JSON file created: {output_file_path}')

with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)

config_data["json_file"] = output_file_path

with open(config_file_path, 'w') as config_file:
    json.dump(config_data, config_file)

logging.info(f'Config file updated: {config_file_path}')
