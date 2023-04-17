import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"

def create_custom_prompt(previous_chapter, query, current_chapter, mode="query"):
    if mode == "title":
        content = f"You wrote before << {previous_chapter} >>, now let's move on and create a prompt of no more than 40 words to develop new interest about <<{query}>>. In this prompt, you read <<{current_chapter}>>, choose the tone for the new chapter, and order to create new practical insights, metaphors, and examples or exercises."
    else:
        content = f"You wrote before << {previous_chapter} >>, now let's move on and create a prompt  of no more than 40 words to develop new interest about <<{query}>>, You must suggest if adding new practical insights, metaphors, and examples on {current_chapter}."

    messages = [
        {"role": "system", "content": "You are the supervisor of the book and a prompt expert."},
        {"role": "user", "content": content},
    ]

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=150,
        stop=None,
    )

    custom_prompt = response['choices'][0]['message']['content'].strip()
    print(f"Custom prompt created: {custom_prompt}")  # Added logging
    return custom_prompt
