import csv
from faker import Faker
import random

from prefect import task, flow
from io import BytesIO
from minio import Minio

@task(name = "Generate Employees", log_prints=True)
def generate_employees(num_employees: int) -> list[dict]:
    # Initialize Faker
    fake = Faker()

    # List of departments and positions
    departments = {
        "Engineering": [
            "Software Engineer",
            "DevOps Engineer",
            "Frontend Developer",
            "Backend Developer",
            "Data Scientist",
            "Machine Learning Engineer",
        ],
        "Marketing": [
            "Marketing Manager",
            "Content Writer",
            "SEO Specialist",
            "Social Media Manager",
        ],
        "Sales": [
            "Sales Representative",
            "Sales Manager",
            "Account Executive",
            "Sales Engineer",
        ],
        "Finance": ["Accountant", "Financial Analyst", "Budget Analyst"],
        "Human Resources": ["HR Specialist", "Recruiter", "Training Coordinator"],
        "Product": ["Product Manager", "UX Designer", "Product Analyst"],
        "Customer Support": ["Support Agent", "Customer Success Manager"],
        "Legal": ["Legal Advisor", "Paralegal"],
        "Operations": [
            "Operations Manager",
            "Logistics Coordinator",
            "Operations Analyst",
        ],
    }
    employees = []
    for i in range(1, num_employees + 1):
        department = random.choice(list(departments.keys()))
        position = random.choice(departments[department])
        employee = {
            "EmployeeID": i,
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "Department": department,
            "Position": position,
            "Email": fake.email(),
        }
        employees.append(employee)
    # Convert employees list to CSV string
    csv_data = ""
    for employee in employees:
        csv_data += f"{employee['EmployeeID']},{employee['FirstName']},{employee['LastName']},{employee['Department']},{employee['Position']},{employee['Email']}\n"

    return csv_data

@task(name = "Write to Minio", log_prints=True)
def write_to_minio(minio_client: Minio, csv_data: list[dict], output_path: str):
    # Upload CSV to Minio
    output_data = csv_data.encode("utf-8")
    minio_client.put_object(
        "landing", output_path, BytesIO(output_data), len(output_data), "text/plain"
    )

    print(f"Fake employee records have been written to {output_path}")

@flow(name= "Fake data generator" ,log_prints=True)
def main(num_employees: int = 60, output_path: str = "Data/employees.csv"):
    MINIO_ENDPOINT = "172.18.0.9:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    minio_client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )
    employees = generate_employees(num_employees)
    write_to_minio(
        minio_client=minio_client, employees_dict=employees, output_path=output_path
    )


if __name__ == "__main__":
    main()
