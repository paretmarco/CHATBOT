from flask import Flask, request, render_template_string
from bs4 import BeautifulSoup
import query_chatbot

app = Flask(__name__)

def read_index_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def parse_html_index(content):
    soup = BeautifulSoup(content, 'html.parser')
    pre_tag = soup.find('pre', {'id': 'book_index_content'})
    return pre_tag.text

@app.route('/', methods=['GET', 'POST'])
def index_input():
    if request.method == 'POST':
        author_name = request.form['author_name']
        book_format = request.form['book_format']
        book_style = request.form['book_style']
        background_info = request.form['background_info']
        index_content = request.form['index_content']

        user_personality = f"I am a chatbot that was designed by {author_name} to write a book about quantum hypnosis. The book is written in a {book_style} style and is available in {book_format}."
        additional_context = f"{background_info} The book is organized as follows:"

        book_title, chapters = parse_index(index_content)
        organized_titles = generate_titles(book_title, chapters)
        collected_texts = []

        api_url = "http://localhost:5001/api/chatbot"

        for title in organized_titles:
            text = query_chatbot.query_chatbot(api_url, title, user_personality, additional_context)
            collected_texts.append(text)

        with open('collected_texts.txt', 'w') as output_file:
            for text in collected_texts:
                output_file.write(text + '\n\n')

        return 'Book content has been generated and saved to collected_texts.txt'
    else:
        form_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Index Input</title>
</head>
<body>
    <h1>Enter book index and additional details</h1>
    <form action="/" method="post">
        <label for="author_name">Author Name:</label>
        <input type="text" id="author_name" name="author_name" required><br><br>
        <label for="book_format">Book Format:</label>
        <input type="text" id="book_format" name="book_format" required><br><br>
        <label for="book_style">Book Style:</label>
        <input type="text" id="book_style" name="book_style" required><br><br>
        <label for="background_info">Background Information:</label>
        <textarea id="background_info" name="background_info" rows="4" cols="50" required></textarea><br><br>
        <label for="index_content">Book Index:</label>
        <textarea id="index_content" name="index_content" rows="20" cols="50" required></textarea><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
'''
        return render_template_string(form_html)

if __name__ == '__main__':
    index_file_path = "book_index.html"
    index_content = read_index_file(index_file_path)

    app.run(host="127.0.0.1", port=5003)

