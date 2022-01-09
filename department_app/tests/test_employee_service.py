import datetime
import random
import unittest
import uuid
from datetime import date

from testbase import TestBase, EMP_COUNT
from werkzeug import exceptions

from department_app.service.employee_service import EmployeeService, Employee
from department_app.service.department_service import Department


class TestEmployeeService(TestBase):

    def test_create_employee(self):
        with self.app.app_context():
            count = Employee.query.count()
            EmployeeService.create_employee(
                name="Random employee name",
                department=Department.query.first(),
                job="Random job",
                birth_date=date(1990, 10, 10),
                salary=500
            )
            self.assertEqual(Employee.query.count(), count+1)

            EmployeeService.create_employee(
                name="Random employee name",
                department=Department.query.first(),
                job="Another job",
                birth_date=date(1991, 10, 10),
                salary=520
            )
            self.assertEqual(Employee.query.count(), count+2)

    def test_get_employee_by_id(self):
        with self.app.app_context():
            emp = Employee.query.first()
            emp_found = EmployeeService.get_employee_by_id(emp_id=emp.id)
            self.assertIsNotNone(emp_found)
            self.assertEqual(emp_found.name, emp.name)

    def test_get_employee_by_id_random(self):
        with self.app.app_context():
            with self.assertRaises(exceptions.NotFound):
                EmployeeService.get_employee_by_id(str(uuid.uuid4()))

    def test_get_all_employees(self):
        with self.app.app_context():
            employees = EmployeeService.get_all_employees()
            self.assertEqual(len(employees), EMP_COUNT)

    def test_update_employee_empty(self):
        with self.app.app_context():
            emp = Employee.query.first()
            name, dep, job, birth_date, salary = emp.name, emp.department, emp.job, emp.birth_date, emp.salary
            EmployeeService.update_employee(emp)
            self.assertEqual(name, emp.name)
            self.assertEqual(dep, emp.department)
            self.assertEqual(job, emp.job)
            self.assertEqual(birth_date, emp.birth_date)
            self.assertEqual(salary, emp.salary)

    def test_update_employee(self):
        with self.app.app_context():
            emp = Employee.query.first()
            new_name = str(uuid.uuid4())
            new_department = random.choice(Department.query.all())
            new_job = str(uuid.uuid4())
            new_birth_date = datetime.date(
                random.randrange(1950, 2004),
                random.randrange(1, 12),
                random.randrange(1, 28)
            )
            new_salary = random.randrange(0, 500)

            EmployeeService.update_employee(emp,
                                            name=new_name,
                                            department=new_department,
                                            job=new_job,
                                            birth_date=new_birth_date,
                                            salary=new_salary
                                            )

            self.assertEqual(emp.name, new_name)
            self.assertEqual(emp.department, new_department)
            self.assertEqual(emp.job, new_job)
            self.assertEqual(emp.birth_date, new_birth_date)
            self.assertEqual(emp.salary, new_salary)

    def test_delete_employee(self):
        with self.app.app_context():
            emp = Employee.query.first()
            EmployeeService.delete_employee(emp)
            self.assertIsNone(Employee.query.get(emp.id))


if __name__ == "__main__":
    unittest.main()
