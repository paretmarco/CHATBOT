import logging
import os
import pinecone
from llama_index import Document, GPTPineconeIndex, SimpleDirectoryReader

# This program has the goal of indexing files and reindexing the WHOLE INDEX
# Configure logging
logging.basicConfig(filename='index_documents.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Set index directory
INDEX_DIR = 'C:/D/documenti/AI/program24/index'
os.makedirs(INDEX_DIR, exist_ok=True)

# Load documents from a directory
logging.info('Loading documents from directory...')
documents = SimpleDirectoryReader('C:/D/documenti/AI/program24/chunker_processed').load_data()

# Set up Pinecone by providing API key and environment
api_key = "93fa5151-3b05-430b-a7a1-78dcf32c7ed3"
environment = "northamerica-northeast1-gcp"
index_name = "project24"
os.environ['PINECONE_API_KEY'] = api_key
pinecone.init(api_key=api_key, environment=environment)
pinecone_index = pinecone.Index(index_name)

# Print the attributes of the first document in the 'documents' list
first_document = documents[0]
print(vars(first_document))

# Construct a Pinecone vector index
logging.info('Constructing Pinecone vector index...')
index = GPTPineconeIndex.from_documents(documents, pinecone_index=pinecone_index)

# Save the index to a file
logging.info('Saving index to disk...')
index.save_to_disk(os.path.join(INDEX_DIR, 'directory_index.json'))

# Deinitialize Pinecone when done
pinecone.deinitialize()
