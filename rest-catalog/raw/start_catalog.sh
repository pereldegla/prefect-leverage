#!/bin/bash

# Variables pour la configuration
CATALOG_NAME="RAW"
WAREHOUSE_LOCATION="s3a://raw/wh"
CATALOG_IMPL="org.apache.iceberg.jdbc.JdbcCatalog"
REST_PORT="8181"
IO_IMPL="org.apache.iceberg.aws.s3.S3FileIO"
S3_ENDPOINT="http://127.0.0.1:9000"
AWS_ACCESS_KEY_ID="minioadmin"
AWS_REGION="us-east-1"
AWS_SECRET_ACCESS_KEY="minioadmin"
URI="jdbc:postgresql://localhost:5432/catalog_raw"
#URI="jdbc:postgresql://localhost:5433/catalog_raw"
JDBC_USER="postgres"
JDBC_PASSWORD="postgres"

# Chemin vers le fichier JAR
JAR_PATH="../iceberg-rest-catalog-all.jar"

# Nom du fichier de log
LOG_FILE="output.log"
PID_FILE="application.pid"  # Nouveau fichier pour stocker le PID

# Commande pour exécuter le JAR en arrière-plan avec les variables
java -jar "$JAR_PATH" CATALOG_NAME="$CATALOG_NAME" \
     WAREHOUSE="$WAREHOUSE_LOCATION" \
     CATALOG-IMPL="$CATALOG_IMPL" \
     REST_PORT="$REST_PORT" \
     IO-IMPL="$IO_IMPL" \
     S3.ENDPOINT="$S3_ENDPOINT" \
     URI="$URI" \
     JDBC.USER="$JDBC_USER" \
     JDBC.PASSWORD="$JDBC_PASSWORD" \
     AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
     AWS_REGION="$AWS_REGION" \
     AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
     -jar "$JAR_PATH" > "$LOG_FILE" 2>&1 &

# Obtention du PID du processus JAR
APPLICATION_PID=$!
echo "$APPLICATION_PID" > "$PID_FILE"  # Stockage du PID dans le fichier

# Affichage du PID du processus JAR
echo "Le processus JAR est lancé en arrière-plan avec le PID : $!"

# Affichage du chemin du fichier de log
echo "Les logs sont enregistrés dans le fichier : $LOG_FILE"
