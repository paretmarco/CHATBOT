import logging
from llama_index import GPTSimpleVectorIndex

# configure logging
logging.basicConfig(filename='index_loader.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# load the index
logging.info('Loading index...')
index = GPTSimpleVectorIndex.load_from_disk('index/directory_index.json')

if __name__ == '__main__':
    while True:
        input("Index loaded successfully. Press Enter to quit...")
