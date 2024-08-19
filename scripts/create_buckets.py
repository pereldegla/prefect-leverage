import os
from minio import Minio
from minio.error import S3Error

# Configuration de l'accès à MinIO
minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Liste des noms de buckets à créer
bucket_names = ["landing", "raw", "table","view"]

# Création des buckets s'ils n'existent pas
for bucket_name in bucket_names:
    if not minio_client.bucket_exists(bucket_name):
        try:
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' créé avec succès.")
        except S3Error as e:
            print(f"Erreur lors de la création du bucket '{bucket_name}': {e}")
    else:
        print(f"Le bucket '{bucket_name}' existe déjà.")
