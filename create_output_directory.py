import os
import sys
from query_processor import process_queries

def sanitize_filename(filename):
    invalid_chars = {'/', '\\', ':', '*', '?', '<', '>', '|'}
    sanitized_name = ''.join(c if c not in invalid_chars else '_' for c in filename)
    return sanitized_name

def create_output_directory(input_directory, output_directory):
    input_file = os.path.join(input_directory, "input_queries.txt")
    
    if not os.path.exists(input_file):
        print("Input file not found.")
        return
    
    with open(input_file, "r", newline='') as infile:
        first_line = infile.readline().strip()
        project_output_directory = os.path.join(output_directory, sanitize_filename(first_line))
        os.makedirs(project_output_directory, exist_ok=True)

    return project_output_directory

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_output_directory.py <input_directory> <output_directory>")
    else:
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]
        project_output_directory = create_output_directory(input_directory, output_directory)
        process_queries(input_directory, project_output_directory)
