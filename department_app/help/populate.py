"""
You can use this module to populate the MySQL database
with a small amount of test departments and employees.
"""

from uuid import uuid4
import datetime
import names
from essential_generators import DocumentGenerator
from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.database import db
import random

DEP_COUNT = 4
EMP_COUNT = 25


def populate_database(of_app):

    text_generator = DocumentGenerator()

    db.init_app(of_app)
    of_app.app_context().push()

    db.drop_all()
    db.create_all()

    with open("department_names.txt") as file:
        department_available_names = file.readlines()

    if len(department_available_names) < DEP_COUNT:
        department_available_names += [f"Department #{k}" for k in range(DEP_COUNT-len(department_available_names))]

    dep_names_chosen = random.sample(department_available_names, DEP_COUNT)
    deps = []
    for i in range(DEP_COUNT):
        deps.append(
            Department(
                id=uuid4(),
                name=f"{dep_names_chosen[i]} Department",
                description=text_generator.paragraph(min_sentences=1, max_sentences=2)[:290]
            )
        )

    with open("job_adjectives.txt") as file:
        job_adjectives = file.readlines()
    with open("job_positions.txt") as file:
        job_positions = file.readlines()

    for i in range(EMP_COUNT):
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


if __name__ == '__main__':
    from department_app.app import app
    populate_database(app)
    print("Database populated!")
