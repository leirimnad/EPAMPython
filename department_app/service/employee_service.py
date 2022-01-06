"""
Includes service class for working with employees.
"""
from uuid import uuid4
from datetime import date

from department_app.models import Employee, Department
from department_app.database import db

# pylint: disable=R0913
class EmployeeService:
    """
    Contains functions for working with employees through a database.
    """

    @staticmethod
    def get_employee_by_id(emp_id) -> Employee:
        """
        Used to get an employee instance using its id.
        @param emp_id: id of the employee to get
        @return: Employee instance or 404 error if employee with the needed id does not exist
        """
        return Employee.query.get_or_404(emp_id)

    @staticmethod
    def get_all_employees() -> list:
        """
        Used to get a list of all the employees.
        @return: a list of Employee instances
        """
        return Employee.query.all()

    @staticmethod
    def create_employee(
            name: str,
            department: Department,
            job: str,
            birth_date: date,
            salary: int
    ) -> Employee:
        """
        Used to create and save a new employee.
        @param name: employee's full name
        @param department: employee's department instance
        @param job: employee's job
        @param birth_date: employee's birthdate
        @param salary: employee's salary
        @return: created employee instance
        """

        emp = Employee(
            id=uuid4(),
            name=name,
            job=job,
            department=department,
            birth_date=birth_date,
            salary=salary
        )
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def update_employee(
            employee: Employee,
            name: str = None,
            department: Department = None,
            job: str = None,
            birth_date: date = None,
            salary: int = None
    ) -> None:
        """
        Used to update employee's information.
        @param employee: employee instance to update
        @param name: new employee's name (optional)
        @param department: new employee's department instance (optional)
        @param job: new employee's job (optional)
        @param birth_date: new employee's birthdate (optional)
        @param salary: new employee's salary (optional)
        """
        if name:
            employee.name = name
        if department:
            employee.department = department
        if job:
            employee.job = job
        if birth_date:
            employee.birth_date = birth_date
        if salary:
            employee.salary = salary
        db.session.commit()

    @staticmethod
    def delete_employee(employee: Employee) -> None:
        """
        Used to delete an employee from the database.
        @param employee: employee to delete
        """
        db.session.delete(employee)
        db.session.commit()
