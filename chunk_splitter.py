import os
import re
from chardet import detect
from nltk.tokenize import word_tokenize, sent_tokenize

input_dir = "C:/D/documenti/AI/program24/chunker-upload"
output_dir = "C:/D/documenti/AI/program24/chunker_split"

target_token_count = 300

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

    sentences = sent_tokenize(text)
    chunks = []

    current_chunk = []
    current_token_count = 0

    for sentence in sentences:
        sentence_tokens = word_tokenize(sentence)
        sentence_token_count = len(sentence_tokens)

        if current_token_count + sentence_token_count <= target_token_count:
            current_chunk.append(sentence)
            current_token_count += sentence_token_count
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_token_count = sentence_token_count

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    for i, chunk in enumerate(chunks):
        book_name = os.path.splitext(input_filename)[0]
        output_filename = f"{book_name}_part_{i+1}.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
