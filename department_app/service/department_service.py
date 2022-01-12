"""
Includes service class for working with departments.
"""

from typing import Optional, Union
from uuid import uuid4
from sqlalchemy.sql import func
from sqlalchemy import asc

from department_app.models import Department, Employee
from department_app.database import db
from .department_validate import DepartmentFieldValidations


class DepartmentService:
    """
    Contains functions for working with departments through a database.
    """

    @staticmethod
    def get_department_by_id(dep_id) -> Department:
        """
        Used to get a department instance using its id.
        @param dep_id: id of the department to get
        @return: Department instance or 404 error if department with the needed id does not exist
        """
        return Department.query.get_or_404(dep_id)

    @staticmethod
    def get_all_departments() -> list:
        """
        Used to get a list of all the departments.
        @return: a list of Department instances
        """
        return Department.query.order_by(asc(Department.name)).all()

    @staticmethod
    def create_department(name: str, description: str) -> Department:
        """
        Used to create and save a new department.
        @param name: department's name
        @param description: department's description
        @return: created department instance
        """

        DepartmentFieldValidations.validate_name(name=name)
        DepartmentFieldValidations.validate_description(description=description)

        dep = Department(id=uuid4(), name=name, description=description)
        db.session.add(dep)
        db.session.commit()
        return dep

    @staticmethod
    def update_department(department, name=None, description=None) -> Department:
        """
        Used to update department's information.
        @param department: department instance to update
        @param name: department's new name (optional)
        @param description: department's new description (optional)
        @return updated department instance
        """

        if name is not None:
            DepartmentFieldValidations.validate_name(name=name)
            department.name = name

        if description is not None:
            DepartmentFieldValidations.validate_description(description=description)
            department.description = description

        db.session.commit()
        return department

    @staticmethod
    def delete_department(department: Department):
        """
        Used to delete a department from the database.
        @param department: department to delete
        """
        if not isinstance(department, Department):
            raise TypeError("Wrong data type")
        db.session.delete(department)
        db.session.commit()

    @staticmethod
    def get_department_average_salary(department: Department) -> Optional[Union[float, int]]:
        """
        Used to calculate average salary for a department.
        @param department: department to calculate an average salary of
        @return: average salary as a float or None if there are no employees in the department
        """
        res = db.session\
            .query(func.avg(Employee.salary).label('average'))\
            .filter(Employee.department == department)\
            .all()
        if res[0][0] is None:
            return None
        ret = float(res[0][0])
        return int(ret) if ret.is_integer() else ret

    @staticmethod
    def get_department_employee_count(department: Department) -> int:
        """
        A method to get an amount of employees working at department.
        @param department: department of the employees
        @return: an amount of employees working at department
        """
        return Employee.query.filter(Employee.department_id == department.id).count()

    @staticmethod
    def get_department_employee_sample(department: Department, size: int) -> list:
        """
        A method to get a sample of employees working at a department.
        @param department: department to get employees of
        @param size: size of the sample
        @return: a list of Employee instances
        """
        return Employee.query.filter(Employee.department_id == department.id).limit(size).all()
