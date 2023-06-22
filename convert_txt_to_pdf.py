import os
from reportlab.pdfgen import canvas

def txt_to_pdf(txt_file, pdf_file):
    # Crea un nuovo PDF
    c = canvas.Canvas(pdf_file)

    # Apri il file di testo con la codifica 'ISO-8859-1'
    with open(txt_file, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()

    # Scrive ogni linea del file di testo nel PDF
    for i, line in enumerate(lines):
        c.drawString(10, 800-i*15, line.strip())

    # Salva il PDF
    c.save()

def convert_directory(dir_path):
    # Ottiene tutti i file nella directory
    files = os.listdir(dir_path)

    # Filtra solo i file di testo
    txt_files = [f for f in files if f.endswith('.txt')]

    # Converte ogni file di testo in un file PDF
    for txt_file in txt_files:
        pdf_file = txt_file[:-4] + '.pdf'
        txt_to_pdf(os.path.join(dir_path, txt_file), os.path.join(dir_path, pdf_file))

# Converte tutti i file di testo nella directory 'my_directory' in file PDF
convert_directory(r'C:\D\documenti\pdf\file vari in txt\altri file 2')
