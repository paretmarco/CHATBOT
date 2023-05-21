import os
import re
from chardet import detect
from nltk.tokenize import word_tokenize, sent_tokenize

input_dir = "C:/D/documenti/AI/program24/chunker_merged_transcripts"
output_dir = "C:/D/documenti/AI/program24/chunker_split_transcripts"

target_token_count = 1000
overlap_token_count = 50

def get_chunks_with_overlap(text, target_token_count, min_word_count):
    chunks = []
    tokens = word_tokenize(text)
    token_length = len(tokens)

    start = 0
    end = target_token_count

    while start < token_length:
        chunk_tokens = tokens[start:end]
        word_count = len(chunk_tokens)

        if word_count >= min_word_count:
            chunk = ' '.join(chunk_tokens)
            chunks.append(chunk)

        start += target_token_count - overlap_token_count
        end = start + target_token_count

    return chunks

for input_filename in os.listdir(input_dir):
    if not input_filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, input_filename)

    # detect file encoding using chardet
    with open(input_path, 'rb') as f:
        encoding = detect(f.read())['encoding']

    # read file using detected encoding
    try:
        with open(input_path, "r", encoding=encoding) as f:
            text = f.read()
    except UnicodeDecodeError:
        print(f"Error: Could not decode the file {input_filename} using detected encoding ({encoding}).")
        print("Trying with 'utf-8' encoding instead.")
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            print(f"Error: Could not decode the file {input_filename} using 'utf-8' encoding.")
            print("Please provide the correct encoding.")
            continue

    text = re.sub(r"\s+", " ", text)
    chunks = get_chunks_with_overlap(text, target_token_count, 800)
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue  # Skip empty chunks

        book_name = os.path.splitext(input_filename)[0]
        # Pad the index with leading zeros
        output_filename = f"{book_name}_part_{i+1:03}.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
