import openai
import json
import time
import re  # Added at the beginning of the script to import the regular expression
from config import OPENAI_API_KEY

# Set up API key and model
openai.api_key = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"

# Function to generate a slogan
def generate_slogan(prompt, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=prompt,
                temperature=0.7,
                max_tokens=200,
                stop=None,
            )
            slogan = response.choices[0].message.content.strip()
            return slogan
        except Exception as e:
            print(f"Error during API call: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Skipping this slogan.")
                return "Error: Unable to generate slogan."

# Function to generate chatbot response completion
def generate_completion(prompt, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=prompt,
                temperature=0.7,
                max_tokens=300,
                stop=None,
            )
            completion = response.choices[0].message.content.strip()
            return completion
        except Exception as e:
            print(f"Error during API call: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Skipping this completion.")
                return "Error: Unable to generate completion."

# Load content from JSON file
json_path = "C:\\D\\documenti\\AI\\program24\\book_created\\book_data.json"
with open(json_path, "r") as f:
    contents = json.load(f)

# Create a single output file in the book_created directory
output_file_path = "C:\\D\\documenti\\AI\\program24\\book_created\\combined_output.txt"
with open(output_file_path, "w", encoding='utf-8') as output_file:
    # Iterate over each item in contents
    for content in contents:
        # Generate slogan
        slogan_prompt = [
            {"role": "system", "content": "You are a creative assistant that generates catchy slogans or citations to introduce the book chapters."},
            {"role": "user", "content": f"Generate a professional and intelligent slogan or citation for {content['title']}."}
        ]
        slogan = generate_slogan(slogan_prompt)

        # Generate chatbot response completion
        chatbot_response_prompt = [
            {"role": "system", "content": "You are a helpful chatbot that provides practical points and suggestions for the book chapters."},
            {"role": "user", "content": f"Complete the last phrase of this text with a metaphor, and a summary in bullet points of other 50 words telling the main points and what a person can get from it without adding concepts but just explaining what is written in: {content['chapter']} {content['results']['chatbot_response']}"},
        ]
        chatbot_response_completion = generate_completion(chatbot_response_prompt)

        # Write output to the single output file
        if re.match(r'^\d+\.\d+', content['title']):
            output_file.write(f"## {content['title']}\n")
        else:
            output_file.write(f"# {content['title']}\n")
        output_file.write(f"{slogan}\n")
        output_file.write("\n")
        output_file.write(f"{content['chapter']}\n")
        output_file.write("\n")
        output_file.write(f"{content['results']['chatbot_response']}\n")
        output_file.write(f"{chatbot_response_completion}\n")
        output_file.write("\n\n")

        # Flush the file buffer to write the content immediately
        output_file.flush()

        print(f"Content generated for {content['title']} and written to combined_output.txt.")