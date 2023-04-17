import logging
import os
from llama_index import GPTSimpleVectorIndex
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # IMPORTANT DONT PUT AWAY THIS LINE CORS HELP COMMUNICATE BETWEEN 5000 and 5001 run before 

# configure logging
logging.basicConfig(filename='search_snippets.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# load the index
logging.info('Loading index...')
index = GPTSimpleVectorIndex.load_from_disk('index/directory_index.json')

# set up Flask app
app = Flask(__name__)
CORS(app)  # Add this line IMPORTANT

# define search API endpoint
@app.route('/api/search', methods=['POST'])
def search_api():
    try:
        logging.info("Received search API request")
        # get query and number of results from request
        query = request.json['query']
        num_results = int(request.json.get('num_results', 1))

        # query the index and take the top-k for similarity - syntax (query, similarity_top_k=X)
        logging.info(f'Querying index with "{query}"...')
        response = index.query(query, similarity_top_k=num_results)
        response_str = str(response)
        logging.info(f'Response is "{response_str}"...')

        # extract relevant snippet from the document
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
        # get query and number of results from user
        query = request.form['query']
        num_results = int(request.form.get('num_results', 1))

        # query the index and take the top-k for similarity - syntax (query, similarity_top_k=X)
        logging.info(f'Querying index with "{query}"...')
        response = index.query(query, similarity_top_k=num_results)
        logging.info(f'Response is "{response}"...')

        # extract relevant snippet from the document
        if response:
            snippet = response
            snippets = [snippet]
        else:
            snippets = []

        # render the search_page.html template with the snippets
        return jsonify({"query": query, "snippets": snippets})
    except Exception as e:
        logging.error(f"Error searching for '{query}': {str(e)}")
        return render_template('search_page.html', query=query, snippets=[])

# define search page
@app.route('/')
def search_page():
    return render_template('search_page.html')

if __name__ == '__main__':
    logging.info('Starting server...')
    host = os.environ.get("FLASK_HOST", "127.0.0.1")  # Add this line to get the host value
    app.run(host=host)  # Update this line to use the host variable