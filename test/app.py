import os
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask import make_response
from flask_cors import CORS
from search_snippets import search_snippets
import logging
import google_sheets_helper
import google_sheets_helper as gsh
from user_operations_gsheet import save_edited_answer  # import function from user_operations

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*', 'methods': ['GET', 'POST', 'PUT', 'DELETE'], 'allow_headers': '*'}})

@app.route('/api/search', methods=['POST'])
def api_search():
    # il tuo codice qui per gestire la richiesta di ricerca API
    return jsonify({'snippets': []})  # ritorna un array vuoto per ora

@app.route('/simple_search', methods=['GET', 'POST'])
def simple_search():
    search_results = None
    if request.method == 'POST':
        query = request.form['query']
        num_results = int(request.form['num_results'])
        verbose = request.form.get('verbose', False) == 'true'

        search_results = search_snippets(query, num_results, verbose)

    return render_template('simple_search_page.html', search_results=search_results)

@app.route('/api/save_draft', methods=['POST'])
def save_draft():
    data = request.get_json()
    text = data.get('text', '')
    with open('drafts/draft_text.txt', 'w') as file:
        file.write(text)
    return jsonify(message="Successfully saved to draft.")

@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = None
    if request.method == 'POST':
        query = request.form['query']
        num_results = int(request.form['num_results'])
        verbose = request.form.get('verbose', False) == 'true'
        
        search_results = search_snippets(query, num_results, verbose)

    return render_template('search_page.html', search_results=search_results)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/save_edited_answer', methods=['POST'])
def save_edited_answer_route():
    # Log the host, port, and route
    host = request.host
    logging.info("Host: %s", host)
    logging.info("Route: %s", request.path)
    # Additional log
    logging.info("Save edited answer route requested")
    logging.info("Request data: %s", request.form)
    edited_answer = request.form['edited_answer']
    user_id = request.form['user_id']

    # Save the edited answer to the Google Sheet
    # Replace 'sheet_id' with the appropriate values
    sheet_id = '1MsUKGRrrBsr-MCQSpyrethObJZD7HpBO1uhz8CRygfI'

    # Get the number of rows in the sheet
    sheet_data = google_sheets_helper.read_data_from_sheet(sheet_id, 'A1:B')
    last_row = len(sheet_data) + 1

    range_name = f'A{last_row}:B{last_row}'
    data_to_write = [[user_id, edited_answer]]
    google_sheets_helper.write_data_to_sheet(sheet_id, range_name, data_to_write)

    resp = jsonify({'message': 'Edited answer saved successfully'})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'

    return resp

    # return {'message': 'Edited answer saved successfully'} vecchia versione


if __name__ == '__main__':
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = os.environ.get("FLASK_PORT", 5002)
    app.run(host=host, debug=True, port=port)
