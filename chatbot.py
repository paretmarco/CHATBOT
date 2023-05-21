import os
import openai
import requests
import json
from flask import Flask, request, jsonify
import logging
import re
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load default values from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

default_max_tokens = config["max_tokens"]
default_author_personality = config["author_personality"]

# per sentenze complete
def is_complete_sentence(sentence):
    # Check if the sentence ends with a punctuation mark
    return bool(re.search(r'[.!?]\s*$', sentence))

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

def search_snippets(query):
    # Log the query
    logging.info(f"Searching snippets for query: {query}")

    search_url = os.environ.get("SEARCH_URL", "http://127.0.0.1:5000/api/search")

    response = requests.post(search_url, json={"query": query})

    logging.info(f"Search response status code: {response.status_code}")

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

import os

def process_chatbot_request(user_input, max_tokens, user_personality, additional_context, model, user_id):
    logging.basicConfig(filename='chatbot.log', level=logging.INFO)

    # Log the user input
    logging.info(f"Processing chatbot request with user_input: {user_input}")

    search_results = search_snippets(user_input)
    logging.info(f"Search results received: {search_results}")

    if search_results and search_results["response"]:
        context = search_results["response"][0]["response"]
    else:
        context = "I couldn't find any relevant information."

    user_message_content = f"{user_input}. To answer, use: {context}"

    if not is_complete_sentence(user_input):
        user_message_content = f"Please complete the following sentence: {user_input}. To answer, consider: {context}"

    available_tokens = 4097 - max_tokens - 100  # reserve some tokens for the response

    # Truncate the user_message_content and context if necessary
    user_message_content = user_message_content[:available_tokens // 2]
    context = context[:available_tokens // 2]

    messages = [
        {"role": "system", "content": user_personality},
        {"role": "assistant", "content": additional_context + " " + context},
        {"role": "user", "content": user_message_content + " please use and adapt this material for your answer being very details"}
    ]

    # Log messages sent to OpenAI API
    logging.info(f"Messages sent to OpenAI API: {messages}")

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=int(max_tokens),
        n=1,
        stop=None,
        temperature=0.8,
    )

    assistant_reply = response.choices[0].message['content']

    # Save the conversation
    filename = f"{user_id}_conversations.json"
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            json.dump({"conversations": []}, f)

    with open(filename, "r+") as f:
        try:
            conversations = json.load(f)["conversations"]
        except (json.JSONDecodeError, KeyError):
            conversations = []

        conversations.append({
            "role": "user",
            "content": user_input
        })
        conversations.append({
            "role": "assistant",
            "content": assistant_reply
        })
        f.seek(0)
        json.dump({"conversations": conversations}, f)
        f.truncate()

    return assistant_reply

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_input = data["user_input"]
        # Ensure user_input doesn't exceed a certain limit, let's say 1000 tokens for simplicity
        if len(user_input.split()) > 1000:
            user_input = ' '.join(user_input.split()[:1000])
            logging.warning(f"User input was longer than 1000 tokens. It has been trimmed.")
        max_tokens = data.get("max_tokens", default_max_tokens)
        user_personality = data.get("user_personality") or default_author_personality
        additional_context = data["additional_context"]
        model = data.get("model", "gpt-3.5-turbo")
        user_id = data.get("user_id", "OWNER")  # Get user_id from the request, with a default value of "OWNER"

        logging.info(f"Received chatbot API request with model {model}, user_id {user_id} and user_input: {user_input}")

        response_text = process_chatbot_request(user_input, max_tokens, user_personality, additional_context, model, user_id)

        logging.info(f"Generated chatbot response: {response_text}")

        return jsonify({"response": response_text})
    except Exception as e:
        logging.error(f"Error in chatbot API: {str(e)}")

        return jsonify({"error": str(e)})

@app.route("/prev_conversations", methods=["GET"])
def prev_conversations():
    user_id = request.args.get("user_id", "OWNER")
    filename = f"{user_id}_conversations.json"

    tokens_to_load = int(request.args.get("tokens", 2000))
    tokens_loaded = 0
    loaded_conversations = []

    if os.path.isfile(filename):
        with open(filename, "r") as f:
            conversations = json.load(f)["conversations"]

        for conversation in reversed(conversations):
            content_length = len(conversation["content"])
            if tokens_loaded + content_length > tokens_to_load:
                break
            loaded_conversations.insert(0, conversation)
            tokens_loaded += content_length

    return jsonify({"conversations": loaded_conversations})

if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")  # Add this line to get the host value
    app.run(host=host, port=5001)