import os
import shutil
from natsort import natsorted

# Get all files in the current directory
all_files = os.listdir()

# Group files by name prefix
file_groups = {}
for file_name in all_files:
    prefix = ''.join(c for c in file_name if not c.isdigit())  # Remove digits to get the prefix
    if prefix not in file_groups:
        file_groups[prefix] = []
    file_groups[prefix].append(file_name)

# Combine files with the same prefix into a single file with ' Improved' added to the prefix
for prefix, file_group in file_groups.items():
    combined_file_name = prefix.strip() + ' Improved'
    
    # Sort the file group naturally before processing
    file_group = natsorted(file_group)

    # Create/overwrite the combined file
    with open(combined_file_name, 'w') as combined_file:
        for file_name in file_group:
            with open(file_name, 'r') as input_file:
                # Copy contents of each file in the group to the combined file in order
                shutil.copyfileobj(input_file, combined_file)

                # Add a newline to separate content from different files
                combined_file.write('\n')
