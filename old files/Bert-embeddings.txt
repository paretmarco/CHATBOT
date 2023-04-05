import os
import torch
from llama_index import Document
from transformers import BertModel, BertTokenizer


# Set up the pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Set the input and output directories
input_dir = 'inputbert'
output_dir = 'outputbert'
os.makedirs(output_dir, exist_ok=True)

# Load the text documents from the input directory
docs = []
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
            text = f.read().strip()
            doc = Document(text)
            docs.append(doc)

# Generate BERT embeddings for each document
for i, doc in enumerate(docs):
    # Tokenize the input text
    input_ids = tokenizer.encode(doc.text, add_special_tokens=True, return_tensors='pt')

    # Generate embeddings using the BERT model
    with torch.no_grad():
        outputs = model(input_ids)
        embeddings = outputs[0][0]  # get the embedding vector for the [CLS] token

    # Save the embeddings to disk as a numpy array
    output_filename = os.path.join(output_dir, f'{i}.npy')
    embeddings_np = embeddings.numpy()
    with open(output_filename, 'wb') as f:
        np.save(f, embeddings_np)
