import logging
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('upload_documents.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file[]')
    for file in files:
        filename = file.filename
        file.save(os.path.join('uploads', filename))
        logger.info(f'File {filename} uploaded successfully')
    return 'Files uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
