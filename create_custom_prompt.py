import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"

def create_custom_prompt(previous_chapter, query, current_chapter, mode="query"):
    prompt_seed = "previous_chapter: << {previous_chapter} >>\ncurrent_chapter: << {current_chapter} >>\nquery: {query}\n\n"
    user_message = "Generate a diverse and creative prompt to explore the topic of the current chapter more effectively. Consider adding practical insights, metaphors, examples, and exercises."
    prompt = prompt_seed.format(previous_chapter=previous_chapter, current_chapter=current_chapter, query=query)

    messages = [
        {"role": "system", "content": "You are the supervisor of the book and a prompt expert."},
        {"role": "user", "content": prompt + user_message},
    ]

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=150,
        stop=["\n"],
        top_p=1,
    )

    custom_prompt = response.choices[0].message['content'].strip()
    return custom_prompt