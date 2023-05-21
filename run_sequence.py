import os

file_list = [
    "query_processor.py",
    "chapter_analysis.py",
    "slogan.py",
    "chunk_to_smooth.py",
    "query_processor_smooth.py",
]

for file_name in file_list:
    os.system(f"python {file_name}")
