import json
import random
import datetime
from string import ascii_lowercase
from uuid import uuid4

from department_app.database.constraints import EmployeeConstraints
from department_app.models import Employee, Department
from testbase import TestBase


class TestEmployeeAPI(TestBase):

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
            else f"{random.randrange(1, 28)}/{random.randrange(1, 12)}/{random.randrange(1950, 2004)}",

            salary=salary if salary is not None
            else random.randrange(200, 800)
        )

    def test_get_employees(self):
        response = self.client.get("/api/employee/")
        self.assertEqual(response.status_code, 200)
        data = str(response.data)
        self.assertTrue(len(data) > 1)

        with self.app.app_context():
            for emp in Employee.query.all():
                self.assertTrue(emp.id in data)
                self.assertTrue(emp.name in data)
                self.assertTrue(emp.department.id in data)
                self.assertTrue(emp.job in data)
                self.assertTrue(str(emp.salary) in data)
                self.assertTrue(str(emp.birth_date.year) in data)
                self.assertTrue(str(emp.birth_date.month) in data)
                self.assertTrue(str(emp.birth_date.day) in data)

    def test_get_employee(self):

        with self.app.app_context():
            emp = Employee.query.first()

        response = self.client.get(f"/api/employee/{emp.id}")
        data = str(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(emp.id in data)
        self.assertTrue(emp.name in data)
        self.assertTrue(emp.department_id in data)
        self.assertTrue(emp.job in data)
        self.assertTrue(str(emp.salary) in data)
        self.assertTrue(str(emp.birth_date.year) in data)
        self.assertTrue(str(emp.birth_date.month) in data)
        self.assertTrue(str(emp.birth_date.day) in data)

    def test_create_employee(self):
        data = self.generate_employee_dict()
        response = self.client.post(f"/api/employee/", data=data)
        self.assertTrue(200 <= response.status_code < 300)
        emp_created = json.loads(response.data)
        with self.app.app_context():
            emp = Employee.query.get(emp_created["id"])
            self.assertEqual(data["name"], emp.name)
            self.assertEqual(data["department_id"], emp.department_id)
            self.assertEqual(data["job"], emp.job)
            self.assertTrue(str(emp.birth_date.year) in data["birth_date"])
            self.assertTrue(str(emp.birth_date.month) in data["birth_date"])
            self.assertTrue(str(emp.birth_date.day) in data["birth_date"])
            self.assertEqual(data["salary"], emp.salary)

    def test_create_employee_no_info(self):
        response = self.client.post(f"/api/employee/")
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_empty_name(self):
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(name=""))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_empty_job(self):
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(job=""))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_empty_salary(self):
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(salary=""))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_empty_birth_date(self):
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(birth_date=""))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_not_unique_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(name=emp.name))
        self.assertTrue(200 <= response.status_code < 300)

    def test_create_employee_not_unique_department(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(department_id=emp.department_id))

        self.assertTrue(200 <= response.status_code < 300)

    def test_create_employee_long_name(self):
        test_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.NAME_MAX_LEN + 10)]
        )
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(name=test_name))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_long_job(self):
        test_job = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.JOB_MAX_LEN + 10)]
        )
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(job=test_job))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_long_name_and_job(self):
        test_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.NAME_MAX_LEN + 10)]
        )
        test_job = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.JOB_MAX_LEN + 10)]
        )
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(name=test_name, job=test_job))
        self.assertTrue(response.status_code >= 400)

    def test_create_employee_born_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        response = self.client.post(f"/api/employee/", data=self.generate_employee_dict(
            birth_date=tomorrow.strftime("%d/%m/%Y")
        ))
        self.assertTrue(response.status_code >= 400)

    def test_patch(self):
        with self.app.app_context():
            emp = Employee.query.first()
        data = self.generate_employee_dict()
        response = self.client.patch(f"/api/employee/{emp.id}", 
                                     data=data)
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_emp = Employee.query.get(emp.id)
            self.assertEqual(data["name"], got_emp.name)
            self.assertEqual(data["department_id"], got_emp.department_id)
            self.assertEqual(data["job"], got_emp.job)
            self.assertTrue(str(got_emp.birth_date.year) in data["birth_date"])
            self.assertTrue(str(got_emp.birth_date.month) in data["birth_date"])
            self.assertTrue(str(got_emp.birth_date.day) in data["birth_date"])
            self.assertEqual(data["salary"], got_emp.salary)

    def test_patch_employee_no_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_data = self.generate_employee_dict()
        new_data.pop("name")
        response = self.client.patch(f"/api/employee/{emp.id}", data=new_data)
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_emp = Employee.query.get(emp.id)
        self.assertEqual(emp.name, got_emp.name)
        self.assertEqual(new_data["job"], got_emp.job)

    def test_patch_employee_empty_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.patch(f"/api/employee/{emp.id}", data=self.generate_employee_dict(name=""))
        self.assertTrue(response.status_code >= 400)

    def test_patch_employee_empty_job(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.patch(f"/api/employee/{emp.id}", data=self.generate_employee_dict(job=""))
        self.assertTrue(response.status_code >= 400)

    def test_patch_employee_long_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.NAME_MAX_LEN + 10)]
        )
        response = self.client.patch(f"/api/employee/{emp.id}", data=self.generate_employee_dict(name=new_name))
        self.assertTrue(response.status_code >= 400)

    def test_patch_employee_long_job(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_job = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.JOB_MAX_LEN + 10)]
        )
        response = self.client.patch(f"/api/employee/{emp.id}", data=self.generate_employee_dict(job=new_job))
        self.assertTrue(response.status_code >= 400)

    def test_patch_employee_long_name_and_job(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.NAME_MAX_LEN + 10)]
        )
        new_job = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.JOB_MAX_LEN + 10)]
        )
        response = self.client.patch(f"/api/employee/{emp.id}",
                                     data=self.generate_employee_dict(name=new_name, job=new_job)
                                     )
        self.assertTrue(response.status_code >= 400)

    def test_patch_employee_not_unique_name(self):
        with self.app.app_context():
            emps = Employee.query.limit(2).all()

        response = self.client.patch(f"/api/employee/{emps[1].id}", data=dict(name=emps[0].name))
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_emp = Employee.query.get(emps[1].id)
            self.assertEqual(emps[0].name, got_emp.name)

    def test_put(self):
        with self.app.app_context():
            emp = Employee.query.first()
        data = self.generate_employee_dict()
        response = self.client.put(f"/api/employee/{emp.id}", data=data)
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_emp = Employee.query.get(emp.id)
            self.assertEqual(data["name"], got_emp.name)
            self.assertEqual(data["department_id"], got_emp.department_id)
            self.assertEqual(data["job"], got_emp.job)
            self.assertTrue(str(got_emp.birth_date.year) in data["birth_date"])
            self.assertTrue(str(got_emp.birth_date.month) in data["birth_date"])
            self.assertTrue(str(got_emp.birth_date.day) in data["birth_date"])
            self.assertEqual(data["salary"], got_emp.salary)

    def test_put_employee_no_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        data = self.generate_employee_dict()
        data.pop("name")
        response = self.client.put(f"/api/employee/{emp.id}", data=data)
        self.assertTrue(response.status_code >= 400)

    def test_put_employee_empty_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.put(f"/api/employee/{emp.id}", data=self.generate_employee_dict(name=""))
        self.assertTrue(response.status_code >= 400)

    def test_put_employee_empty_job(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.put(f"/api/employee/{emp.id}", data=self.generate_employee_dict(job=""))
        self.assertTrue(response.status_code >= 400)

    def test_put_employee_long_name(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.NAME_MAX_LEN + 10)]
        )
        response = self.client.put(f"/api/employee/{emp.id}", data=self.generate_employee_dict(name=new_name))
        self.assertTrue(response.status_code >= 400)

    def test_put_employee_long_job(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_job = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.JOB_MAX_LEN + 10)]
        )
        response = self.client.put(f"/api/employee/{emp.id}", data=self.generate_employee_dict(job=new_job))
        self.assertTrue(response.status_code >= 400)

    def test_put_employee_long_name_and_job(self):
        with self.app.app_context():
            emp = Employee.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.NAME_MAX_LEN + 10)]
        )
        new_job = "".join(
            [random.choice(ascii_lowercase) for _ in range(EmployeeConstraints.JOB_MAX_LEN + 10)]
        )
        response = self.client.put(f"/api/employee/{emp.id}",
                                   data=self.generate_employee_dict(name=new_name, job=new_job)
                                   )
        self.assertTrue(response.status_code >= 400)

    def test_put_employee_not_unique_name(self):
        with self.app.app_context():
            emps = Employee.query.limit(2).all()
        response = self.client.put(f"/api/employee/{emps[1].id}", data=self.generate_employee_dict(name=emps[0].name))
        self.assertTrue(200 <= response.status_code < 300)

    def test_delete_employee(self):
        with self.app.app_context():
            emp = Employee.query.first()
        response = self.client.delete(f"/api/employee/{emp.id}")
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            self.assertIsNone(Employee.query.get(emp.id))

    def test_delete_employee_that_not_exists(self):
        response = self.client.delete(f"/api/employee/{uuid4()}")
        self.assertTrue(response.status_code >= 400)
