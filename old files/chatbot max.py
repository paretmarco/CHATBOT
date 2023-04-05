import os
import openai
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

def search_snippets(query):

 # Log the query
    logging.info(f"Searching snippets for query: {query}")

    search_url = "http://127.0.0.1:5000/api/search"
    response = requests.post(search_url, json={"query": query})
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def process_chatbot_request(user_input, max_tokens, user_personality, additional_context):
    # Log the user input
    logging.info(f"Processing chatbot request with user_input: {user_input}")

    search_results = search_snippets(user_input)

    logging.info(f"Search results received: {search_results}")
    if search_results and search_results["response"]:
        context = search_results["response"][0]["response"]
    else:
        context = "I couldn't find any relevant information."

    messages = [
        {"role": "system", "content": user_personality},
        {"role": "assistant", "content": additional_context + " " + context},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=int(max_tokens),
        n=1,
        stop=None,
        temperature=0.8,
    )

    # check this point:     assistant_reply = response.choices[0].message['content']
    assistant_reply = response.choices[0].text

    # Save the conversation
    with open("prev_conversations.json", "r+") as f:
        conversations = json.load(f)["conversations"]
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
        max_tokens = data["max_tokens"]
        user_personality = data["user_personality"]
        additional_context = data["additional_context"]

        logging.info(f"Received chatbot API request with user_input: {user_input}")

        response_text = process_chatbot_request(user_input, max_tokens, user_personality, additional_context)

        logging.info(f"Generated chatbot response: {response_text}")

#       old was return jsonify({"error": str(e)})
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)})

# old was : @app.route("/prev_conversations", methods=["GET"])
@app.route("/load_previous_conversations", methods=["GET"])
def load_previous_conversations():
    tokens_to_load = int(request.args.get("tokens", 1500))
    tokens_loaded = 0
    loaded_conversations = []

    with open("prev_conversations.json", "r") as f:
        conversations = json.load(f)["conversations"]

    for conversation in reversed(conversations):
        content_length = len(conversation["content"])
        if tokens_loaded + content_length > tokens_to_load:
            break
        loaded_conversations.insert(0, conversation)
        tokens_loaded += content_length

    previous_conversations = ""
    for conversation in loaded_conversations:
        if conversation["role"] == "user":
            previous_conversations += "<b>You:</b> " + conversation["content"] + "<br>"
        else:
            previous_conversations += "<b>AI:</b> " + conversation["content"] + "<br>"

    return jsonify({"previous_conversations": previous_conversations})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
