FROM python:3.9-slim

RUN apt-get update && apt-get install -y coreutils

WORKDIR /app

COPY requirements.txt requirements.txt
COPY config.json /app/config.json
RUN pip install -r requirements.txt

COPY . .

RUN mkdir /logs

EXPOSE 5000
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
EXPOSE 8000

CMD ["sh", "-c", "python search_snippets.py 2>&1 | tee /logs/search_snippets.log & python chatbot.py 2>&1 | tee /logs/chatbot.log & python app.py --port 5002 & gunicorn --workers 4 --bind 0.0.0.0:5003 web_app:app 2>&1 | tee /logs/web_app.log"]

