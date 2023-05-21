import pyperclip

file_list = ["web_app.py", "templates/index.html"]  # Add or modify the file names in this list

def combina_contenuti_file(file_list):
    combined_content = f"Ecco qui i file: {', '.join(file_list)}\n\n"
    for file_name in file_list:
        try:
            with open(file_name, "r", encoding='utf-8') as infile:
                file_content = infile.read()
                combined_content += f"File: {file_name}\n{file_content}\n\n"
        except FileNotFoundError:
            print(f"Errore: {file_name} non trovato.")
    return combined_content

if __name__ == "__main__":
    contenuto_combinato = combina_contenuti_file(file_list)
    pyperclip.copy(contenuto_combinato)
    print("Contenuto combinato dei file copiato con successo nel buffer di Windows!")

