# Basis-Image
FROM python:3.11-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Port für FastAPI
EXPOSE 8000

# Testbefehl
RUN ["pytest", "-v"]

# Startbefehl
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]