import logging
from llama_index import GPTSimpleVectorIndex
import openai
from flask import Flask, render_template, request

# configure logging
logging.basicConfig(filename='search_documents.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# load the index
logging.info('Loading index...')
index = GPTSimpleVectorIndex.load_from_disk('index/directory_index.json')

# set up OpenAI API key
with open('config/openai.txt', 'r') as f:
    openai.api_key = f.read().strip()

# set up Flask app
app = Flask(__name__)

# define search route
@app.route('/search')
def search():
    # get query from user
    query = request.args.get('q')

    # query the index
    logging.info(f'Querying index with "{query}"...')
    response = []
    query_bundle = index._get_query_bundle(query)
    if query_bundle.embedding is not None:
        response = index.query(query)

    # extract relevant snippets from the documents
    snippets = []
    for r in response:
        snippets.append(r.document.content[r.start:r.end])
    
    # format snippets for display
    formatted_snippets = '<br>'.join(snippets)

    # generate response using OpenAI's GPT
    prompt = f"What is {query}?"
    logging.info(f"Generating response with prompt: '{prompt}'")
    gpt_response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # extract the answer from GPT response
    answer = gpt_response.choices[0].text.strip()

    # render the search_results.html template with the response
    return render_template('search_documents.html', query=query, answer=answer, snippets=formatted_snippets)

if __name__ == '__main__':
    app.run(debug=True)
