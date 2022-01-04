"""
You can use this module to populate the MySQL database
with a small amount of test departments and employees.
"""

from uuid import uuid4
import datetime
from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app import db


db.drop_all()
db.create_all()


d1 = Department(id=uuid4(), name="Dep1", description="Some description.")
d2 = Department(id=uuid4(), name="Dep2", description="Some description..")
d3 = Department(id=uuid4(), name="Dep3", description="Some description...")

e1 = Employee(
    id=uuid4(),
    name="Employee1",
    job="The Job",
    department=d1,
    salary=500,
    birth_date=datetime.date(1990, 6, 6)
)
e2 = Employee(
    id=uuid4(),
    name="Employee2",
    job="The Job",
    department=d2,
    salary=500,
    birth_date=datetime.date(1990, 6, 6)
)
e3 = Employee(
    id=uuid4(),
    name="Employee3",
    job="The Job",
    department=d2,
    salary=540,
    birth_date=datetime.date(1990, 6, 6)
)
e4 = Employee(
    id=uuid4(),
    name="Employee4",
    job="The Job",
    department=d3,
    salary=1040,
    birth_date=datetime.date(1890, 6, 6)
)


db.session.add(d1)
db.session.add(d2)
db.session.add(d3)


db.session.commit()
