import csv
from io import StringIO
import openai  # Assuming you have access to GPT-4 API
from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def generate_victor_hugo_style_text(text):
    prompt = f"Parafrasa e scrivi con lo stile di Victor Hugo: {text}"
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100,  # Modify as needed
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

# Route for the new search page (v2)
@app.route('/search_page_v2', methods=['GET'])
def search_page_v2():
    return render_template('search_page_v2.html')

@app.route('/submit_question', methods=['POST'])
def submit_question():
    question = request.form['question']
    return redirect(url_for('search_page_v2', question=question))

@app.route('/store_answer', methods=['POST'])
def store_answer():
    answer = request.form['answer']
    with sqlite3.connect("answers.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO answers (answer) VALUES (?)", (answer,))
        con.commit()
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(port=5002)

# Step 2: Define the content of the csv file
csv_content = "..."

# Step 3: Parse the csv file
csv_file = StringIO(csv_content)
csv_reader = csv.reader(csv_file, delimiter=',')

# Step 4: Extract the text to work on
text_to_work_on = [row[1] for row in csv_reader][1:]

# Step 5: Implement the 'generate_victor_hugo_style_text()' function (already defined)

# Step 6: Rewrite each text in the style of Victor Hugo
rewritten_texts = []

for text in text_to_work_on:
    new_text = generate_victor_hugo_style_text(text)
    rewritten_texts.append(new_text)

# Step 7: Add interesting insights and exercises to each rewritten text
insight_text = "aggiungi spunti interessanti"
exercise_text = "e se ci sono esercizi scrivili in fondo per punti."

for rewritten_text in rewritten_texts:
    rewritten_text += f"\n\n{insight_text}\n\n{exercise_text}"
