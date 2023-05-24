# BOOK PROCESSING - for sending the questions to the chatbot and get the answer
import json
import os
import requests
import logging
from google_sheets_helper import read_data_from_sheet, find_sheet_by_title, write_data_to_sheet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_query_to_chatbot(question, title, additional_context):
    chatbot_url = "http://127.0.0.1:5001/api/chatbot"
    prompt = f"queste domande spiegale meglio con un paragrafo di integrazione indipendente aggiuntivo e con in cima il titolo della ### {question} ###, esse sono ### {question} ###\n Rispondi in linguaggio: - {language} - e sii molto pregnante e chiaro nella prima riga per dare il senso del paragrafo. Personalizza parlando in prima persona opure utilizza il voi oppure il tu. Puoi utilizzare vari formati. Storia (vi racconto ora una storia per capire come), domande dei clienti (alcuni clienti domandano) a seconda di quello che è più appropriato."
    data = {
        "user_input": prompt,
        "max_tokens": 400,
        "additional_context": additional_context
    }
    response = requests.post(chatbot_url, json=data)
    
    logging.info(f"Prompt sent: {prompt}")
    
    if response.status_code == 200:
        json_data = response.json()
        if 'response' in json_data:
            logging.info(f"Answer received: {json_data['response']}")
            return json_data["response"]
        else:
            logging.error("'response' key is missing in the chatbot JSON data.")
            return None
    else:
        logging.error(f"Error in chatbot response: {response.status_code}")
        return None

def process_questions(sheet_id, read_range):
    logging.info(f"Google Sheet ID: {sheet_id}")
    sheet_data = read_data_from_sheet(sheet_id, read_range)

    book_data = []

    for record in sheet_data:
        if not record[7]:  # If column H is empty, stop processing
            break

        title = record[1]  # Read the chapter title from column B (index 1)
        chapter_content = record[2]  # Read the chapter content from column C (index 2)
        relevant_questions = list(filter(lambda x: x and x.rstrip().endswith('?') and x[0].isdigit() and x[1] == '.', record[7].strip().split('\n')))

        chapter = {
            "title": title,
            "chapter": chapter_content,
            "relevant_questions": relevant_questions
        }

        book_data.append(chapter)

    answer_index = 2

    for index, record in enumerate(book_data):
        title = record.get("title", "")
        relevant_questions = record.get("relevant_questions", [])
        logging.info(f"Extracted questions: {relevant_questions}")
        faqs = []

        for q_index, question in enumerate(relevant_questions):
            logging.info(f"Processing question: {question}")

            # Send the question to the chatbot and get the response
            chatbot_response = send_query_to_chatbot(question, title, additional_context)

            if chatbot_response:
                faqs.append({"question": question, "answer": chatbot_response})
                logging.info(f"Chatbot response for question: '{question}' is '{chatbot_response}'")

                # Write the answer to the Google Sheet in columns I and J
                if answer_index % 2 == 0:
                    write_range = f"I{answer_index // 2 + 1}"
                else:
                    write_range = f"J{(answer_index + 1) // 2}"

                write_data_to_sheet(sheet_id, write_range, [[chatbot_response]])
                answer_index += 1

        # Save the FAQ section in the record
        record["FAQ"] = faqs

        logging.info(f"JSON file updated with results for questions in chapter {index + 1}.")

if __name__ == "__main__":
    with open('config.json') as config_file:
        config = json.load(config_file)
        additional_context = config['additional_context']
        sheet_name = config['sheet_name']  # Read the sheet_name from the config file
        language = config['language']

    # Find the Google Sheet with the specified name
    folder_id = "1O4__jxbTubCObzCCn08oPe0bc0DlP-uO"  # Replace with the folder ID of the "AI_CREATED_BOOKS" directory
    sheet_id = find_sheet_by_title(sheet_name, folder_id)
    
    READ_RANGE = "A2:H"  # Adjust this range based on your sheet's structure
    process_questions(sheet_id, READ_RANGE)

