import os
import re

input_dir = "C:/D/documenti/AI/program24/chunker_merged_transcripts"
output_dir = "C:/D/documenti/AI/program24/chunker_mergedglobal_transcripts"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_files = os.listdir(input_dir)

def extract_root_name(filename):
    return re.sub(r"_part_\d+_processed_modified\.txt", "", filename)

root_names = sorted(list(set(extract_root_name(f) for f in input_files)))

for root_name in root_names:
    related_files = sorted([f for f in input_files if extract_root_name(f) == root_name], key=lambda x: int(re.findall(r'\d+', x.split("_part_")[1])[0]))
    
    combined_chunks = []
    
    for input_filename in related_files:
        input_path = os.path.join(input_dir, input_filename)
        with open(input_path, "r", encoding="utf-8") as input_file:
            chunk = input_file.read()
            combined_chunks.append(chunk)
    
    output_filename = f"{root_name}_combined.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write("\n\n".join(combined_chunks))
        print(f"Chunks for {root_name} have been combined into {output_filename}")
