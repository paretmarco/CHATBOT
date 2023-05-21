import requests
import json

app_script_url = "https://script.google.com/macros/s/AKfycbxETV2aXWIU3CEAruMwRfE3ijRLMYOunBpBaRGiFpISmjR0BtNvW7Bwph4cegyFmcCDlQ/exec"

# Replace the sample data with the actual data your script expects
sample_data = {
    "user_input": "Hello, how are you?"
}

response = requests.post(app_script_url, json=sample_data)

# Check if the response is valid JSON
try:
    json_response = response.json()
    print("Valid JSON response received:")
    print(json.dumps(json_response, indent=2))
except json.JSONDecodeError:
    print("Invalid JSON response received:")
    print(response.text)
