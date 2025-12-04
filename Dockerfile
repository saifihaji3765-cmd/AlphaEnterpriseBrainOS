FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY backend/ ./backend
COPY frontend/ ./frontend
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
ENV FLASK_APP=backend/app.py
ENV PORT=8000
EXPOSE 8000
CMD ["python","backend/app.py"]
