import os
import json
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('book_modify.html')

@app.route('/book_data')
def book_data():
    with open("C:\\D\\documenti\\AI\\program24\\book_created\\book_data.json", "r", encoding="utf-8") as f:
        book_data = json.load(f)
    return jsonify(book_data)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
