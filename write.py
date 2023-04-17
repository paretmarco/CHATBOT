file_list = ["app.py", "chatbot.py", "Dockerfile", "docker-compose.yml", "config.py", "templates/search_page.html", "static/main.js", "templates/search_page_options.html"]  # Add or modify the file names in this list

output_file = "all_files.txt"

with open(output_file, "w") as outfile:
    for file_name in file_list:
        try:
            with open(file_name, "r") as infile:
                file_content = infile.read()
                outfile.write(f"File: {file_name}\n{file_content}\n")
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")

print(f"Combined content of files written to {output_file}")
