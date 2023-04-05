import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

def generate_response(prompt, model="text-davinci-002", max_tokens=150):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def chatbot():
    print("Welcome to the GPT-4 Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        prompt = f"User: {user_input}\nChatbot:"
        response = generate_response(prompt)
        print(f"Chatbot: {response}")

chatbot()
