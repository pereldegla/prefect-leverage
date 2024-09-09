import csv
from faker import Faker
import random
from prefect import task, Flow
from minio import Minio

# Initialize Faker
fake = Faker()

# List of departments and positions
departments = {
    'Engineering': ['Software Engineer', 'DevOps Engineer', 'Frontend Developer', 'Backend Developer', 'Data Scientist', 'Machine Learning Engineer'],
    'Marketing': ['Marketing Manager', 'Content Writer', 'SEO Specialist', 'Social Media Manager'],
    'Sales': ['Sales Representative', 'Sales Manager', 'Account Executive', 'Sales Engineer'],
    'Finance': ['Accountant', 'Financial Analyst', 'Budget Analyst'],
    'Human Resources': ['HR Specialist', 'Recruiter', 'Training Coordinator'],
    'Product': ['Product Manager', 'UX Designer', 'Product Analyst'],
    'Customer Support': ['Support Agent', 'Customer Success Manager'],
    'Legal': ['Legal Advisor', 'Paralegal'],
    'Operations': ['Operations Manager', 'Logistics Coordinator', 'Operations Analyst']
}

# Number of fake employees to generate
num_employees = 30

# CSV file name
output_file = 'employees.csv'

# Generate fake employees
employees = []
for i in range(1, num_employees + 1):
    department = random.choice(list(departments.keys()))
    position = random.choice(departments[department])
    employee = {
        'EmployeeID': i,
        'FirstName': fake.first_name(),
        'LastName': fake.last_name(),
        'Department': department,
        'Position': position,
        'Email': fake.email()
    }
    employees.append(employee)

# Write to Minio
minio_client = Minio('minio.example.com',
                     access_key='YOUR_ACCESS_KEY',
                     secret_key='YOUR_SECRET_KEY',
                     secure=True)

# Convert employees list to CSV string
csv_data = ''
for employee in employees:
    csv_data += f"{employee['EmployeeID']},{employee['FirstName']},{employee['LastName']},{employee['Department']},{employee['Position']},{employee['Email']}\n"

# Upload CSV to Minio
minio_client.put_object('my-bucket', output_file, csv_data.encode('utf-8'))


print(f'{num_employees} fake employee records have been written to {output_file}')
