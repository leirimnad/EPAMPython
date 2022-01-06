"""
You can use this module to populate the MySQL database
with a small amount of test departments and employees.
"""

from uuid import uuid4
import datetime
from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.database import db
import random

DEP_COUNT = 3
EMP_COUNT = 4


def populate_database(of_app):

    db.init_app(of_app)
    of_app.app_context().push()

    db.drop_all()
    db.create_all()

    deps = []
    for i in range(DEP_COUNT):
        deps.append(Department(id=uuid4(), name=f"Dep{i}", description="Some description."))

    for i in range(EMP_COUNT):
        Employee(
            id=uuid4(),
            name=f"Employee{i}",
            job="The Job",
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
