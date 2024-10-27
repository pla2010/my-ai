FROM python:3.11

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt ./
COPY ia.py ./

# Met à jour pip et installe les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir numpy

# Commande pour exécuter ton application
CMD ["python", "ia.py"]
