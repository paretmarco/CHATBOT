import requests
import json
import sys

def query_chatbot(api_url, query, user_personality, additional_context):
    payload = {
        'user_input': query,
        'max_tokens': 150,
        'user_personality': user_personality,
        'additional_context': additional_context
    }

    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['response']
    else:
        raise ValueError(f"Error querying chatbot API: {response.status_code}")

api_url = "http://localhost:5004/api/search"  # Port updated to 5004
collected_texts = []

try:
    with open('collected_texts.txt', 'w') as output_file:
        for index, title in enumerate(organized_titles, start=1):
            print(f"Processing title {index} of {len(organized_titles)}: {title}")
            text = query_chatbot(api_url, title)
            collected_texts.append(text)
            
            # Save the text to the output file immediately
            output_file.write(text + '\n\n')

            # Check for keyboard interrupt
            if KeyboardInterrupt:
                print("Book creation process interrupted.")
                break

except KeyboardInterrupt:
    print("Book creation process interrupted.")
