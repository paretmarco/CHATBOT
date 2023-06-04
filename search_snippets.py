# File: search_snippets.py - its goal is to extract relevant snippets
import logging
import os
os.environ["PINECONE_API_KEY"] = "93fa5151-3b05-430b-a7a1-78dcf32c7ed3"
import pinecone
from llama_index import GPTPineconeIndex
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# configure logging
logging.basicConfig(filename='search_snippets.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Set Pinecone API key and environment
pinecone_api_key = "93fa5151-3b05-430b-a7a1-78dcf32c7ed3"
pinecone_environment = "northamerica-northeast1-gcp"
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

# Load Pinecone index
index_name = "project24"
pinecone_index = pinecone.Index(index_name)

# Add the class definition here
class CustomGPTPineconeIndex(GPTPineconeIndex):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Create GPTPineconeIndex instance
index = CustomGPTPineconeIndex([], pinecone_index=pinecone_index)

# set up Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# define search API endpoint
@app.route('/api/search', methods=['POST'])
def search_api():
    logging.info("function: search_api")
    logging.info(request.json)  # This will log the received data in your Flask server's console
    try:
        logging.info("Received search API request")
        query = request.json['query']
        num_results = int(request.json.get('num_results', 1))
        logging.info(f'Querying index with "{query}"...')
        response = index.query(query, similarity_top_k=num_results)
        response_str = str(response)
        logging.info(f'Response is "{response_str}"...')
        if response:
            snippet_text = response_str
            logging.info(f'Snippet text is "{snippet_text}"')
            snippets = [{"response": snippet_text}]
        else:
            snippets = []
        return jsonify({'query': query, 'response': snippets})
    except Exception as e:
        logging.error(f"Error searching for '{query}': {str(e)}")
        return jsonify({'error': str(e), 'error_message': f"Error searching for '{query}': {str(e)}"}), 500

# define search route
@app.route('/search', methods=['POST'])
def search_snippets():
    try:
        query = request.form['query']
        num_results = int(request.form.get('num_results', 1))
        logging.info(f'Querying index with "{query}"...')
        response = index.query(query, similarity_top_k=num_results)
        logging.info("{response}")
        if response:
            snippet = response
            logging.info(f'Answer is "{response}"...')
            snippets = [snippet]
        else:
            snippets = []
        return render_template('search_page.html', query=query, snippets=snippets)
    except Exception as e:
        logging.error(f"Error searching for '{query}': {str(e)}")
        return render_template('search_page.html', query=query, snippet='')

@app.route('/')
def search_page():
    return render_template('search_page.html')

@app.route('/api/snippets', methods=['GET'])  # for server.js
def get_snippets():
    try:
        query = request.form['query']
        num_results = int(request.form.get('num_results', 1))
        logging.info(f'Querying index with "{query}"...')
        response = index.query(query, similarity_top_k=num_results)
        logging.info("{response}")
        if response:
            snippet = response
            logging.info(f'Answer is "{response}"...')
            snippets = [snippet]
        else:
            snippets = []
        return render_template('search_page.html', query=query, snippets=snippets)
    except Exception as e:
        logging.error(f"Error searching for '{query}': {str(e)}")

    return jsonify({'snippets': snippets})

@app.route('/simple_search')
def simple_search_page():
    return render_template('simple_search_page.html')

if __name__ == '__main__':
    logging.info('Starting server...')
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    app.run(host=host)