import logging
import os
import pinecone
import glob
import json
from llama_index import Document, GPTPineconeIndex, SimpleDirectoryReader

def load_documents_from_json_directory(directory):
    documents = []
    for file_path in glob.glob(os.path.join(directory, '*.json')):
        logging.info(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                doc_data = json.load(f)
            except json.decoder.JSONDecodeError:
                logging.error(f"Invalid JSON file: {file_path}")
                continue

            # Use the file name without extension as the doc_id if it's not in the JSON file
            doc_id = doc_data.get('doc_id', os.path.splitext(os.path.basename(file_path))[0])
            document = Document(doc_data['content'], doc_id=doc_id)
            documents.append(document)
    return documents

# Configure logging
logging.basicConfig(filename='index_documents.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Set index directory
INDEX_DIR = 'C:/D/documenti/AI/program24/index'
os.makedirs(INDEX_DIR, exist_ok=True)

# Load documents from a directory
logging.info('Loading documents from JSON directory...')
documents = load_documents_from_json_directory('C:/D/documenti/AI/program24/chunker_processed')

# Set up Pinecone by providing API key and environment
api_key = "93fa5151-3b05-430b-a7a1-78dcf32c7ed3"
environment = "northamerica-northeast1-gcp"
index_name = "project24"
os.environ['PINECONE_API_KEY'] = api_key
pinecone.init(api_key=api_key, environment=environment)
pinecone_index = pinecone.Index(index_name)

# Construct a Pinecone vector index
logging.info('Constructing Pinecone vector index...')
index = GPTPineconeIndex.from_documents(documents, pinecone_index=pinecone_index)

# Save the index to a file
logging.info('Saving index to disk...')
index.save_to_disk(os.path.join(INDEX_DIR, 'directory_index.json'))
