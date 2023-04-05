import subprocess
import sys
from threading import Thread

# Define a function to run a script in a separate thread
def run_script(script_name):
    subprocess.call([sys.executable, script_name])

if __name__ == '__main__':
    # Define script names
    scripts = ['chatbot.py', 'search_snippets.py', 'app.py']

    # Create threads to run scripts
    threads = [Thread(target=run_script, args=(script_name,)) for script_name in scripts]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
