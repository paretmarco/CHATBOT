import openai
import os

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

MODEL = "gpt-3.5-turbo"

def create_book_index(draft_text):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert writer."},
            {"role": "user", "content": f"Create an index for a book based on this draft text: {draft_text}. Divide the book into chapters, paragraphs, and subchapters with numbers like 1 Chapter 1, 1.1 Paragraph, 1.1.1 Subparagraph."},
            {"role": "assistant", "content": ""},
        ],
        temperature=0.5,
    )
    
    index_text = response.choices[0].message.content.strip()
    
    with open("input/input_queries.txt", "w", encoding="utf-8") as index_file:
        index_file.write(index_text)
    
    print("Index created and saved in input/input_queries.txt")

# Read the draft text from the "drafts" directory
with open("drafts/draft_text.txt", "r", encoding="utf-8") as draft_file:
    draft_text = draft_file.read()

# Call the create_book_index function with the draft_text
create_book_index(draft_text)

