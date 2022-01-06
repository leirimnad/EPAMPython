"""
Module that defines the REST API for the Employee model.
"""

from flask_restful import Resource
from department_app.service import EmployeeService


class EmployeeListAPI(Resource):
    """
    Defines the REST API for the full list of employees.
    """

    @staticmethod
    def get():
        """
        Get request handler.
        @return: list of employees dictionaries
        """
        employees = EmployeeService.get_all_employees()
        return [emp.to_dict() for emp in employees]


class EmployeeAPI(Resource):
    """
    Defines the REST API for a single employee query.
    """

    @staticmethod
    def get(emp_id):
        """
        Get request handler.
        @param emp_id: id of the employee to get
        @return: employees as a dictionary or 404 error if employee does not exist
        """
        emp = EmployeeService.get_employee_by_id(emp_id=emp_id)
        return emp.to_dict()
