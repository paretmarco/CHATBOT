import os

def compare_directories(dir1, dir2):
    files_dir1 = set(os.listdir(dir1))
    files_dir2 = set(os.listdir(dir2))

    common_files = files_dir1.intersection(files_dir2)
    return common_files

def delete_files(files, directory):
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            os.remove(file_path)
            print(f"Deleted {file} from {directory}")
        except OSError:
            print(f"Error deleting {file} from {directory}")

dir1 = r"C:\D\documenti\AI\program24\chunker-upload"
dir2 = r"C:\D\documenti\AI\program24\chunker_uploaded_done"

common_files = compare_directories(dir1, dir2)

if common_files:
    print("Files already present in 'chunker_uploaded_done' directory:")
    for file in common_files:
        print(f"- {file}")

    # Delete common files from 'chunker-upload' directory
    delete_files(common_files, dir1)
else:
    print("No files are present in both directories.")
