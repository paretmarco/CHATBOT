import subprocess

def run_script(script_name):
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

if __name__ == "__main__":
    app_process = run_script('app.py')
    chatbot_process = run_script('chatbot.py')
    search_snippets_process = run_script('search_snippets.py')

    # If you want main.py to wait until all processes are done, uncomment the following lines
    # app_process.wait()
    # chatbot_process.wait()
    # search_snippets_process.wait()

    # If you want main.py to print output from all scripts, uncomment the following lines
    # print(app_process.communicate())
    # print(chatbot_process.communicate())
    # print(search_snippets_process.communicate())

