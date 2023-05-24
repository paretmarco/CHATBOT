# BOOK PROCESSING - THIS IS THE SEQUENCE OF THE RELATIVE PROGRAMS - SLOGAN CHANGED NAME book_slogan
import os

file_list = [
    "query_processor.py",
    "chapter_analysis.py",
    "book_slogan.py",
    "chunk_to_smooth.py",
    "query_processor_smooth.py",
]

for file_name in file_list:
    os.system(f"python {file_name}")
