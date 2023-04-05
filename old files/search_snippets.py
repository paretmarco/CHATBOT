import logging
from llama_index import GPTSimpleVectorIndex
from flask import Flask, render_template, request

# configure logging
logging.basicConfig(filename='search_snippets.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# load the index
logging.info('Loading index...')
index = GPTSimpleVectorIndex.load_from_disk('index/directory_index.json')

# set up Flask app
app = Flask(__name__)

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
        logging.info("{response}")

        # extract relevant snippet from the document
        if response:
            snippet = response
            logging.info(f'Answer is "{response}"...')
            snippets = [snippet]
        else:
            snippets = []

        # render the search_page.html template with the snippets
        return render_template('search_page.html', query=query, snippets=snippets)
    except Exception as e:
        logging.error(f"Error searching for '{query}': {str(e)}")
        return render_template('search_page.html', query=query, snippet='')

@app.route('/')
def search_page():
    return render_template('search_page.html')

if __name__ == '__main__':
    logging.info('Starting server...')
    app.run()