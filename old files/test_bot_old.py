from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def search_page():
    return render_template('search_page.html')

@app.route('/search', methods=['POST'])
def search_snippets():
    query = request.form['query']
    num_results = int(request.form['num_results'])
    print(f"Search Snippets received query: {query}, num_results: {num_results}")
    return jsonify({"status": "ok"})

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    user_input = request.json['user_input']
    print(f"Received user input: {user_input}")
    return jsonify({'user_input': user_input, 'assistant_response': 'Test response'})

if __name__ == '__main__':
    app.run(port=5001)
