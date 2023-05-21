import openai
import os
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"

def load_keywords():
    try:
        with open("drafts/keywords.txt", "r", encoding="utf-8") as f:
            return [kw.strip() for kw in f.readlines()]
    except FileNotFoundError:
        print("keyword.txt not found.")
        return []

def load_target_public():
    try:
        with open("Drafts/target_public.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("target_public.txt not found.")
        return ""

keywords = load_keywords()
target_public = load_target_public()

categories = {
    "Mito o Leggenda": "Scegliendo tra queste parole: {keyword} di quali miti o leggendo possiamo parlare?",
    "Storia": "Partendo da {keyword} Quale è la storia più interessante che possiamo dire su alcuni dei seguenti concetti: {keyword}?",
    "Pratica": "una pratica curiosa relativa a {keyword}?",
    "Estetica": "cosa significa {keyword} a livello dell'estetica?",
    "Esercizio": "Sei un chatbot che crea domande relative a quali di questi temi è più interessante parlare: {keyword}?",
    "Scienze": "Cosa dicono le scienze su {keyword}?",
    "Personaggi": "Analizza {keyword} e crea domande su personaggi famosi al riguardo?",
    "Collegamenti": "Che collegamenti sono importanto per i seguenti concetti: {keyword}?",
    "Citazione": "Quale è una citazione possibile relativa ad uno dei seguenti concetti: {keyword}?",
    "Emozione": "Quali sono le emozioni collegate ad uno dei seguenti concetti: {keyword} e come vanno vissute?"
}

def generate_questions(keyword):
    questions = []
    for category, question_template in categories.items():
        question = question_template.format(keyword=keyword)
        print(f"Generated question: '{question}'")  # Add this line to log generated questions
        questions.append(question)
    return questions

def extract_best_questions(lines):
    selected_questions = []
    for line in lines:
        line = line.strip()
        print(f"Adding line: '{line}'")  # Debug line
        selected_questions.append(line)
    return selected_questions

def select_best_questions(questions, max_questions=40):
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "1 Quali sono le abitudini o le pratiche associate a X?. 2 In che modo Y si posiziona all'interno del contesto generale? etc..."},
        {"role": "user", "content": f"Devi utilizzare solo queste parole e devi selezionare tra queste le {max_questions} domande più utili, interessanti e curiose scegliendo tra le seguenti:\n" + "\n".join(questions) + "per {target_public}."},
        {"role": "user", "content": f"Scegli solo tra queste. Quali sono le {max_questions} migliori domande per {target_public}? Ogni domanda deve contenere una sola keyword tra queste : {keyword}"}
    ]
    
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=prompt,
        temperature=0.5,
        max_tokens=1300,
        stop=None,
    )
    
    # Log the response
    print(f"IA response: {response.choices[0].message.content}")
    
    # Replace the following line
    # selected_question_indices = extract_question_indices(response.choices[0].message.content)
    # with
    selected_questions = extract_best_questions(response.choices[0].message.content.split("\n"))
    
    return selected_questions

all_questions = []

for keyword in keywords:
    questions = generate_questions(keyword)
    all_questions.extend(questions)

best_questions = select_best_questions(all_questions)

print(f"Le migliori {len(best_questions)} domande sono:")
for question in best_questions:
    print(f"  {question}")

def save_best_questions(questions, filename="drafts/best_questions_2.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for question in questions:
            f.write(f"{question}\n")

save_best_questions(best_questions)

