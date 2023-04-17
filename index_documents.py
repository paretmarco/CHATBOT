import logging
import os
from llama_index import Document, GPTSimpleVectorIndex, SimpleDirectoryReader

# this program has as goal to index files and reindex the WHOLE INDEX 
# configure logging
logging.basicConfig(filename='index_documents.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# set index directory
INDEX_DIR = 'C:/D/documenti/AI/program24/index'
os.makedirs(INDEX_DIR, exist_ok=True)

# load documents from a directory
logging.info('Loading documents from directory...')
documents = SimpleDirectoryReader('C:/D/documenti/AI/program24/uploads').load_data()

# construct a simple vector index
logging.info('Constructing vector index...')
index = GPTSimpleVectorIndex.from_documents(documents)

# save the index to a file
logging.info('Saving index to disk...')
index.save_to_disk(os.path.join(INDEX_DIR, 'directory_index.json'))
