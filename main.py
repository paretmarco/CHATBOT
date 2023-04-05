import os
from chatbot_handler import handle_chat_query
from query_loader import load_queries_from_file

# Set up your API key for the language model provider (e.g., OpenAI)
api_key = os.environ["OPENAI_API_KEY"]

# Read the input_queries.txt file
queries = load_queries_from_file("input/input_queries.txt")

# Iterate over the queries and process each one
for query in queries:
    print(f"Handling query: {query}")
    response = handle_chat_query(query, api_key)
    print(f"Response: {response}\n")
