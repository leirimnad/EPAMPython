import json
import random
import datetime
from uuid import uuid4

from department_app.models import Employee, Department
from testbase import TestBase, decode_escapes
from faker import Faker
fake = Faker()


class TestEmployeeViews(TestBase):

    def generate_employee_dict(self, name=None, department_id=None, job=None, birth_date=None, salary=None) -> dict:
        with self.app.app_context():
            dep = random.choice(Department.query.all())
        return dict(
            name=name if name is not None
            else str(uuid4()),

            department_id=department_id if department_id is not None
            else dep.id,

            job=job if job is not None
            else str(uuid4()),

            birth_date=birth_date if birth_date is not None
            else fake.date_time_between(start_date='-30y', end_date='now').strftime('%d/%m/%Y'),

            salary=salary if salary is not None
            else random.randrange(200, 800)
        )

    def test_get_employees(self):
        response = self.client.get("/employee/")
        self.assertEqual(response.status_code, 200)
        data = decode_escapes(response.get_data(as_text=True))
        self.assertTrue(len(data) > 1)

    def test_create_employee_get(self):
        response = self.client.get(f"/employee/add")
        self.assertTrue(200 <= response.status_code < 300)

    def test_create_employee(self):
        data = self.generate_employee_dict()
        response = self.client.post(f"/employee/add", data=data)
        self.assertTrue(200 <= response.status_code < 400)

    def test_create_employee_born_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        response = self.client.post(f"/employee/add", data=self.generate_employee_dict(
            birth_date=tomorrow.strftime("%d/%m/%Y")
        ))
        self.assertTrue(200 <= response.status_code < 300)

    def test_delete_employee(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.get(f"/employee/{emp.id}/delete")
        self.assertTrue(300 <= response.status_code < 400)
        with self.app.app_context():
            self.assertIsNone(Employee.query.get(emp.id))

    def test_delete_employee_that_not_exists(self):
        response = self.client.delete(f"/employee/{uuid4()}/delete")
        self.assertTrue(response.status_code >= 400)
