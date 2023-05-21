import logging
import os
import json
import glob
from llama_index import Document, GPTSimpleVectorIndex, SimpleDirectoryReader

# configure logging
logging.basicConfig(filename='index_documents.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# set base directory
BASE_DIR = 'C:/D/documenti/AI/program24'

# set index directory
INDEX_DIR = os.path.join(BASE_DIR, 'index')
os.makedirs(INDEX_DIR, exist_ok=True)

def load_documents_from_json_directory(directory):
    documents = []
    for file_path in glob.glob(os.path.join(directory, '*.json')):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                doc_data = json.load(f)
            except json.decoder.JSONDecodeError:
                logging.error(f"Invalid JSON file: {file_path}")
                continue
            document = Document(doc_data['content'], doc_id=doc_data['doc_id'])
            documents.append(document)
    return documents

# load documents from a directory
logging.info('Loading documents from directory...')
documents = SimpleDirectoryReader(os.path.join(BASE_DIR, 'chunker_processed')).load_data()

# load new documents from the JSON directory
logging.info('Loading new documents from JSON directory...')
new_documents = load_documents_from_json_directory(os.path.join(BASE_DIR, 'json_output'))

# load the existing index from disk or create a new one if it doesn't exist
index_path = os.path.join(INDEX_DIR, 'directory_index.json')
if os.path.exists(index_path):
    logging.info('Loading existing index from disk...')
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
else:
    logging.info('Creating new index...')
    index = GPTSimpleVectorIndex([])

# insert new documents into the existing index
logging.info('Inserting new documents into the existing index...')
for doc in new_documents:
    index.insert(doc)

# construct a simple vector index
logging.info('Constructing vector index...')
index = GPTSimpleVectorIndex(documents + new_documents)

# save the updated index to disk
logging.info('Saving updated index to disk...')
index.save_to_disk(index_path)
