import os
import re
import json
import openai
import logging
from nltk.tokenize import sent_tokenize
from transformers import GPT2Tokenizer

logging.basicConfig(level=logging.INFO)

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_text(prompt, model="gpt-3.5-turbo"):
    max_length = 4096 - len(tokenizer.encode("[ChatGPT] ")) - 2
    prompt_tokens = tokenizer.encode(prompt)
    truncated_prompt_tokens = prompt_tokens[:max_length]
    truncated_prompt = tokenizer.decode(truncated_prompt_tokens)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Generate relevant and creative text based on the given input. You put relevant infos in order to better understand and index the text."},
            {"role": "user", "content": truncated_prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

input_dir = "C:/D/documenti/AI/program24/chunker_split"
output_dir = "C:/D/documenti/AI/program24/chunker_processed"

for input_filename in os.listdir(input_dir):
    logging.info(f"Processing {input_filename}")
    
    if not input_filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, input_filename)
    with open(input_path, "r", encoding="utf-8") as f:
        chunk = f.read()

    chunk_number = int(re.search(r"_part_(\d+)", input_filename).group(1))

    prev_chunk_filename = re.sub(r"_part_(\d+)", f"_part_{chunk_number - 1}", input_filename)
    next_chunk_filename = re.sub(r"_part_(\d+)", f"_part_{chunk_number + 1}", input_filename)

    prev_chunk = ""
    if os.path.exists(os.path.join(input_dir, prev_chunk_filename)):
        with open(os.path.join(input_dir, prev_chunk_filename), "r", encoding="utf-8") as f:
            prev_chunk = f.read()

    next_chunk = ""
    if os.path.exists(os.path.join(input_dir, next_chunk_filename)):
        with open(os.path.join(input_dir, next_chunk_filename), "r", encoding="utf-8") as f:
            next_chunk = f.read()

    logging.info("Generating title")
    title_input = f"Create a title for this text of no more than 10 words in order to make clear the meaning of the text: {prev_chunk} {chunk} {next_chunk}"
    title_text = generate_text(title_input)

    logging.info("Generating first phrase")
    first_phrase_input = f"Create an introductory phrase for this text of no more than 25 words. This phrase should give a meaning to the chunk, give the relevant names of the people in it and make easy to situate: {prev_chunk[-3:]} {chunk}"
    first_phrase_text = generate_text(first_phrase_input)

    logging.info("Generating last phrase")
    last_phrase_input = f"Create a concluding phrase for this text of no more than 40 words. This phrase should be useful for the reader and in some way practical. If the text is an exercise write the completion and the steps: {chunk} {next_chunk}"
    last_phrase_text = generate_text(last_phrase_input)

    book_name = os.path.splitext(input_filename)[0]
    output_filename = f"{book_name}_processed.json"
    output_path = os.path.join(output_dir, output_filename)

    logging.info("Writing output file")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": title_text,
            "first_phrase": first_phrase_text,
            "content": chunk,
            "last_phrase": last_phrase_text
        }, f, ensure_ascii=False, indent=2)

    logging.info(f"Finished processing {input_filename}")
