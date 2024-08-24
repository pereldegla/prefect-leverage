FROM python:3.10-slim

# Installation des dépendances depuis requirements.txt
WORKDIR /app
COPY scripts/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copie des scripts dans le conteneur
COPY scripts /app

# Définition de la commande de démarrage
CMD ["sh", "-c", "python /app/create_databases.py && python /app/create_buckets.py"]