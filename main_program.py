import subprocess

def run_program(file_name):
    subprocess.Popen(['python', file_name])

if __name__ == '__main__':
    run_program('app.py')
    run_program('search_snippets.py')
    run_program('chatbot.py')
