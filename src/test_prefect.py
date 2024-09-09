from prefect import flow, task
from minio import Minio
import pandas as pd

MINIO_URL = "http://172.18.0.9:9000"
MINIO_ENDPOINT = "172.18.0.9:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_IS_SECURE = False
########################### REST Catalog  ###########################
RAW_CATALOG_URL = "http://172.18.0.10"
RAW_CATALOG_PORT = "8181"
RAW_CATALOG_NAME = "RAW"

TABLE_CATALOG_URL = "http://172.18.0.5"
TABLE_CATALOG_PORT = "8182"
TABLE_CATALOG_NAME = "TABLE"

LANDING_BUCKET_NAME = "landing"

@task(name = "Read CSV", log_prints=True)
def read_csv(filename: str = "employees.csv"):
    minio_client = Minio(
                endpoint=MINIO_ENDPOINT,
                access_key=MINIO_ACCESS_KEY,
                secret_key=MINIO_SECRET_KEY,
                secure=MINIO_IS_SECURE,
            )
    data = minio_client.get_object(
        bucket_name=LANDING_BUCKET_NAME,
        object_name=filename,
    )
    df = pd.read_csv(data)
    return df

@task(log_prints=True)
def add(x, y):
    return x + y

@task(log_prints=True)
def multiply(x, y):
    return x * y

@flow(log_prints=True)
def main():
    a = add(1, 2)
    b = multiply(a, 3)
    print(a)

main()