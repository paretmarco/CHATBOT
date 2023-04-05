import os
import re
import math
import openai
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set up your OpenAI API key
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Function to generate text using GPT-3.5-turbo
def generate_text(prompt, model="gpt-3.5-turbo", timeout=60):
    max_length = 4096 - len(tokenizer.encode("[ChatGPT] ")) - 2
    prompt_tokens = tokenizer.encode(prompt)
    text_parts = []
    
    for i in range(0, len(prompt_tokens), max_length):
        truncated_prompt_tokens = prompt_tokens[i:i+max_length]
        truncated_prompt = tokenizer.decode(truncated_prompt_tokens)

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Generate relevant and creative text based on the given input."},
                {"role": "user", "content": truncated_prompt}
            ],
            timeout=timeout
        )
        text_parts.append(response.choices[0].message['content'].strip())

    return " ".join(text_parts)

# specify the path to the input directory
input_dir = "C:/D/documenti/AI/program24/chunker-upload"

# specify the chunk size
chunk_size = 500

# loop over all files in the input directory
for input_filename in os.listdir(input_dir):
    # make sure the file is a text file
    if not input_filename.endswith(".txt"):
        continue

    # read in the text file
    input_path = os.path.join(input_dir, input_filename)
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # preprocess the text (remove extra spaces, line breaks, etc.)
    text = re.sub(r"\s+", " ", text)

    # divide the text into chunks
    tokens = tokenizer(text, return_tensors="pt", add_special_tokens=False).input_ids.squeeze()
    num_chunks = math.ceil(len(tokens) / chunk_size)
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, tokens.shape[0])
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

    # generate titles, first phrases, and last phrases for each chunk
    titles = []
    first_phrases = []
    last_phrases = []
    for i, chunk in enumerate(chunks):
        # get the preceding and following chunks (if available)
        if i > 0:
            prev_chunk = chunks[i-1]
        else:
            prev_chunk = ""
        if i < len(chunks)-1:
            next_chunk = chunks[i+1]
        else:
            next_chunk = ""

        # generate the title
        title_input = f"Create a title for this text: {prev_chunk} {chunk} {next_chunk}"
        title_text = generate_text(title_input[:4096])
        titles.append(title_text)

        # generate the first phrase
        first_phrase_input = f"Create an introductory phrase for this text: {prev_chunk} {chunk}"
        first_phrase_text = generate_text(first_phrase_input[:4096])
        first_phrases.append(first_phrase_text)

        # generate the last phrase
        last_phrase_input = f"Create a concluding phrase for this text: {chunk} {next_chunk}"
        last_phrase_text = generate_text(last_phrase_input[:4096])
        last_phrases.append(last_phrase_text)

        # write the chunk to a separate file
        output_dir = "C:/D/documenti/AI/program24/chunker_chunked"
        book_name = os.path.splitext(input_filename)[0]
        output_filename = f"{book_name}_{i+1}.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {titles[i]}\n\n")
            f.write(f"First phrase: {first_phrases[i]}\n\n")
            f.write(chunk)
            f.write(f"\n\nLast phrase: {last_phrases[i]}\n\n")
