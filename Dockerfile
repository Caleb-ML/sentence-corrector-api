# Verwende ein schlankes Python-Image
FROM python:3.10-slim

# Umgebungsvariablen setzen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Arbeitsverzeichnis im Container
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt kopieren und installieren
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Projektdateien kopieren
COPY . .

# Django-Server starten
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
