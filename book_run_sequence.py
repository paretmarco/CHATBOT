# BOOK PROCESSING - THIS IS THE SEQUENCE OF THE RELATIVE PROGRAMS - SLOGAN CHANGED NAME book_slogan
# book_creator.py to create the index
# book_create_chapters.py to create the chapters
import os

file_list = [
    "query_processor.py",
    "chapter_analysis.py",
    "book_slogan.py",
    "chunk_to_smooth.py",
    "query_processor_smooth.py",
    "chunk_to_smooth.py",
    "query_processor_human.py",    
]

for file_name in file_list:
    os.system(f"python {file_name}")
