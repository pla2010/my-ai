FROM python:3.9

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt ./
COPY ia.py ./

# Met à jour pip et installe les dépendances
RUN pip install --upgrade pip
RUN cat requirements.txt && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Commande pour exécuter ton application
CMD ["python", "ia.py"]
