import os
import shutil
from natsort import natsorted

# Set the origin directory and get all files in it
origin_dir = "chunker_processed_transcripts"
all_files = os.listdir(origin_dir)

# Define the target directory for the combined files
target_dir = "chunker_merged_transcripts"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Group files by name prefix
file_groups = {}
for file_name in all_files:
    prefix = ''.join(c for c in file_name if not c.isdigit())  # Remove digits to get the prefix
    if prefix not in file_groups:
        file_groups[prefix] = []
    file_groups[prefix].append(file_name)

# Combine files with the same prefix into a single file with ' Improved' added to the prefix
for prefix, file_group in file_groups.items():
    combined_file_name = prefix.strip() + ' Improved.txt'

    # Sort the file group naturally before processing
    file_group = natsorted(file_group)

    # Create the combined file directly in the target directory
    target_file_path = os.path.join(target_dir, combined_file_name)
    with open(target_file_path, 'w') as combined_file:
        for file_name in file_group:
            file_path = os.path.join(origin_dir, file_name)
            with open(file_path, 'r') as input_file:
                # Copy contents of each file in the group to the combined file in order
                shutil.copyfileobj(input_file, combined_file)

                # Add a newline to separate content from different files
                combined_file.write('\n')
