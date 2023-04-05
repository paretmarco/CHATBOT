import os
import openai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import logging

# Configure logging to show messages in the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler(filename='chatbot.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)

# Set up the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def search_page():
    return render_template('search_page.html')

@app.route('/search', methods=['POST'])
def search_snippets():
    query = request.form['query']
    num_results = int(request.form['num_results'])
    logging.info(f"Search Snippets received query: {query}, num_results: {num_results}")

    # Your existing search_snippets function code here
    return "Success"

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    try:
        user_input = request.json['user_input']
        logging.info(f"Received user input: {user_input}")

        # Send the user query to the search_snippets.py API
        search_response = requests.post('http://localhost:5000/search', json={'query': user_input, 'num_results': 1})

        if search_response.status_code == 200:
            search_data = search_response.json()
            search_snippets = search_data['snippets']
            search_context = " ".join(search_snippets)
            logging.info(f"Search context: {search_context}")
        else:
            search_context = "We speak mainly about non-verbal techniques"
            logging.warning("Failed to get search context, using default context")

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "assistant", "content": search_context},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        assistant_response = openai_response.choices[0].message.content.strip()
        logging.info(f"Assistant response: {assistant_response}")
        response = jsonify({'user_input': user_input, 'assistant_response': assistant_response})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    except Exception as e:
        logging.error(f"Error processing chatbot request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
