FROM python:3.9-slim

WORKDIR /app

COPY config.py ./

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY index/ index/

COPY . .

CMD ["sh", "-c", "exec python search_snippets.py & exec python chatbot.py & exec python app.py"]
