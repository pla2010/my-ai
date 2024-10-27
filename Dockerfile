# Utiliser une image de base appropriée
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de dépendances dans l'image
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Commande pour démarrer l'application
CMD ["python", "ia.py"]
