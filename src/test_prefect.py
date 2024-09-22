from prefect import flow, task
from prefect.artifacts import create_table_artifact
from minio import Minio
import pandas as pd
from dotenv import load_dotenv
import os
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Access the variables
MINIO_URL = os.getenv("MINIO_URL")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
RAW_CATALOG_URL = os.getenv("RAW_CATALOG_URL")
RAW_CATALOG_PORT = os.getenv("RAW_CATALOG_PORT")
RAW_CATALOG_NAME = os.getenv("RAW_CATALOG_NAME")
TABLE_CATALOG_URL = os.getenv("TABLE_CATALOG_URL")
TABLE_CATALOG_PORT = os.getenv("TABLE_CATALOG_PORT")
TABLE_CATALOG_NAME = os.getenv("TABLE_CATALOG_NAME")
MINIO_IS_SECURE = True if os.getenv("MINIO_IS_SECURE") == "True" else False
LANDING_BUCKET_NAME = os.getenv("LANDING_BUCKET_NAME")


@task(name="Read CSV", log_prints=True)
def read_csv(
    minio_client: Minio,
    filename: str = "employees.csv",
):
    data = minio_client.get_object(
        bucket_name=LANDING_BUCKET_NAME,
        object_name=filename,
    )
    df = pd.read_csv(data)
    return df


@task(name="Count Employees", log_prints=True)
def count_per_key(df: pd.DataFrame, key: str, grouped_column: str):
    return df.groupby(key).size().reset_index(name=grouped_column)


@task(name="Create Table Artifact", log_prints=True)
def save_table_artifact(df: pd.DataFrame, description: str):
    # Convert the DataFrame to a list of dictionaries
    table_dict = df.to_dict(orient="records")
    create_table_artifact(
        key="myartifact", table=table_dict, description=description
    )


@task(name="Write to Minio", log_prints=True)
def write_to_minio(minio_client: Minio, df: pd.DataFrame, filename: str):
    output_data = df.to_csv(index=False).encode("utf-8")
    minio_client.put_object(
        bucket_name=LANDING_BUCKET_NAME,
        object_name=filename,
        data=BytesIO(output_data),
        length=len(output_data),
        content_type="text/csv",
    )


@flow(name="Prefect test flow", log_prints=True)
def main(
    input_filename: str,
    output_filename: str,
):
    minio_client = Minio(
        endpoint=MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_IS_SECURE,
    )
    df = read_csv(minio_client=minio_client, filename=input_filename)
    employee_per_department = count_per_key(df=df, key="Department", grouped_column="EmployeeCount")
    employee_per_position = count_per_key(df=df, key="Position", grouped_column="EmployeeCount")
    save_table_artifact(
        df=employee_per_position, description="Employee count per position"
    )
    write_to_minio(
        minio_client=minio_client,
        df=employee_per_department,
        filename=output_filename,
    )


if __name__ == "__main__":
    input_filename = "Data/employees.csv"
    output_filename = "Data/employee_per_department.csv"

    main(
        input_filename=input_filename,
        output_filename=output_filename,
    )
