import json
import random
from datetime import datetime, timedelta

# Helper functions to generate random data
def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y%m%d')

def random_name():
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_email(name):
    domains = ["example.com", "mail.com", "test.com", "email.com"]
    return f"{name.split()[0].lower()}.{name.split()[1].lower()}@{random.choice(domains)}"

def random_phone():
    return f"555-{random.randint(1000, 9999)}"

# Generate random data
num_students = 500
num_employees = 500

students_data = {
    "personal_info": {},
    "grades": {}
}

employees_data = {
    "contact_info": {},
    "department": {}
}

start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 1, 1)
departments = ["HR", "Engineering", "Marketing", "Sales"]
managers = ["Sarah", "Mike", "Jane", "John"]

for i in range(1, num_students + 1):
    date = random_date(start_date, end_date)
    students_data["personal_info"][str(i)] = {
        "name": [random_name(), date],
        "age": [str(random.randint(20, 30)), date]
    }
    students_data["grades"][str(i)] = {
        "math": [random.choice(["A", "B", "C", "D"]), date],
        "science": [random.choice(["A", "B", "C", "D"]), date]
    }

for i in range(101, 101 + num_employees):
    date = random_date(start_date, end_date)
    name = random_name()
    employees_data["contact_info"][str(i)] = {
        "email": [random_email(name), date],
        "phone": [random_phone(), date]
    }
    employees_data["department"][str(i)] = {
        "name": [random.choice(departments), date],
        "manager": [random.choice(managers), date]
    }

data = {
    "tables": {
        "students": students_data,
        "employees": employees_data
    }
}

# Save to file
with open('data/initial_data.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Initial data generated and saved to data/initial_data.json")
