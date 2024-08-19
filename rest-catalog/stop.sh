#!/bin/bash

# Fichier contenant le PID de l'application
PID_FILE="application.pid"

# Lire le PID à partir du fichier
if [ -f "$PID_FILE" ]; then
    APPLICATION_PID=$(cat "$PID_FILE")
else
    echo "Le fichier de PID ($PID_FILE) n'a pas été trouvé."
    exit 1
fi

# Vérifier si le processus est en cours d'exécution en utilisant le PID
if ps -p $APPLICATION_PID > /dev/null; then
    echo "Arrêt de l'application avec le PID : $APPLICATION_PID"
    kill "$APPLICATION_PID"
else
    echo "Le processus avec le PID $APPLICATION_PID n'est pas en cours d'exécution."
    exit 1
fi
