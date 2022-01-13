"""
You can use this module to populate the MySQL database
with a small amount of test departments and employees.
"""
import argparse
from uuid import uuid4
import datetime
import names
from essential_generators import DocumentGenerator
from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.database import db
import random
import re
import os

with open(os.path.join(os.path.dirname(__file__), "department_names.txt")) as file:
    department_available_names = file.readlines()
    department_available_names = [line.rstrip() for line in department_available_names]
with open(os.path.join(os.path.dirname(__file__), "job_adjectives.txt")) as file:
    job_adjectives = file.readlines()
    job_adjectives = [line.rstrip() for line in job_adjectives]
with open(os.path.join(os.path.dirname(__file__), "job_positions.txt")) as file:
    job_positions = file.readlines()
    job_positions = [line.rstrip() for line in job_positions]

text_generator = DocumentGenerator()


def populate_database(of_app, *, dep_count=4, emp_count=10):
    global department_available_names, job_adjectives, job_positions, text_generator

    db.init_app(of_app)
    of_app.app_context().push()

    db.drop_all()
    db.create_all()

    if len(department_available_names) < dep_count:
        department_available_names += [f"Department #{k}" for k in range(dep_count-len(department_available_names))]

    dep_names_chosen = random.sample(department_available_names, dep_count)
    deps = []
    for i in range(dep_count):
        deps.append(
            Department(
                id=uuid4(),
                name=f"{dep_names_chosen[i]} Department",
                description=generate_description()
            )
        )

    for i in range(emp_count):
        Employee(
            id=uuid4(),
            name=names.get_full_name(),
            job=f"{random.choice(job_adjectives)} {random.choice(job_positions)}",
            department=random.choice(deps),
            salary=500+random.randrange(-200, 200, 10),
            birth_date=datetime.date(
                random.randrange(1950, 2004),
                random.randrange(1, 12),
                random.randrange(1, 28)
            )
        )

    for dep in deps:
        db.session.add(dep)

    db.session.commit()


def generate_description():
    res = text_generator.paragraph(min_sentences=1, max_sentences=2)
    res = re.sub(r"[^a-zA-Z0-9 \-:,.!?-]", "", res)
    return res[:290]


if __name__ == '__main__':
    from department_app.app import app

    parser = argparse.ArgumentParser(description='Populate database with test departments and employees')
    parser.add_argument("-d", nargs=1, type=int, help='amount of departments to generate', default=4)
    parser.add_argument("-e", nargs=1, type=int, help='amount of employees to generate', default=25)

    args = parser.parse_args()

    populate_database(app, dep_count=args.d, emp_count=args.e)
    print("Database populated!")
