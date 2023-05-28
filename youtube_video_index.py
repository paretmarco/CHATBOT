import logging
import os
from llama_index import Document, GPTSimpleVectorIndex, SimpleDirectoryReader

# configure logging
logging.basicConfig(filename='create_index.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def create_index():
    # ensure 'youtube_uploads' directory exists
    if not os.path.exists('youtube_uploads'):
        logging.error("Directory 'youtube_uploads' does not exist.")
        return

    # Load documents from the directory
    logging.info('Loading documents from directory...')
    documents = SimpleDirectoryReader('youtube_uploads').load_data()

    # Construct a simple vector index
    logging.info('Constructing vector index...')
    index = GPTSimpleVectorIndex.from_documents(documents)

    # Ensure 'youtube_video_index' directory exists
    os.makedirs('youtube_video_index', exist_ok=True)

    # Save the index to a file
    logging.info('Saving index to disk...')
    index.save_to_disk('youtube_video_index/directory_index.json')

create_index()


