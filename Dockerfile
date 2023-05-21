FROM python:3.9-slim

RUN apt-get update && apt-get install -y coreutils

WORKDIR /app

COPY requirements.txt requirements.txt
COPY config.json /app/config.json
RUN pip install -r requirements.txt

COPY . .

RUN mkdir /logs

CMD ["sh", "-c", "python search_snippets.py 2>&1 | tee /logs/search_snippets.log & python chatbot.py 2>&1 | tee /logs/chatbot.log & python app.py & gunicorn --workers 4 --bind 0.0.0.0:5002 web_app:app 2>&1 | tee /logs/web_app.log"]

