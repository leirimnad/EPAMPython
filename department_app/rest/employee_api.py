"""
Module that defines the REST API for the Employee model.
"""
import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import exc as sqlalchemy_err

from department_app.service import EmployeeService, DepartmentService
from .utils import format_exception_message


class EmployeeListAPI(Resource):
    """
    Defines the REST API for getting the full list of employees and creating a new one.
    """

    @staticmethod
    def get():
        """
        Get request handler.
        @return: list of employees dictionaries
        """
        emps = EmployeeService.get_all_employees()
        return [emp.to_dict() for emp in emps]

    @staticmethod
    def post():
        """
        Put request handler.
        @return: new employee as dictionary, if one was successfully created
        """
        name = request.form['name']
        department = DepartmentService.get_department_by_id(request.form['department_id'])
        job = request.form['job']
        birth_date_str = request.form['birth_date']
        try:
            birth_date = None if birth_date_str is None \
                else datetime.datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        except (TypeError, ValueError):
            return format_exception_message(
                exception="Birth date must be provided as %d/%m/%Y"
            ), 400

        if not request.form['salary'].isnumeric():
            return format_exception_message(exception="Salary must be numeric"), 400
        salary = int(request.form['salary'])

        try:
            new_emp = EmployeeService.create_employee(
                name=name, department=department, job=job,
                birth_date=birth_date, salary=salary
            )

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400

        return new_emp.to_dict(), 202


class EmployeeAPI(Resource):
    """
    Defines the REST API for a single employee query.
    """

    @staticmethod
    def get(emp_id):
        """
        Get request handler.
        @param emp_id: id of the employee to get
        @return: employee as a dictionary or 404 error if employee does not exist
        """
        emp = EmployeeService.get_employee_by_id(emp_id=emp_id)
        return emp.to_dict()

    @staticmethod
    def patch(emp_id):
        """
        Patch request handler, for editing an employee.
        If a parameter is None, it is not changed in the employee.
        @param emp_id: id of the employee to update
        @return: edited employee as a dictionary or 404 error if employee does not exist
        """
        try:
            emp = EmployeeService.get_employee_by_id(emp_id=emp_id)

            name = request.form.get("name", default=None)
            department_id = request.form.get("department_id", default=None)
            department = None if department_id is None \
                else DepartmentService.get_department_by_id(department_id)
            job = request.form.get("job", default=None)
            birth_date_str = request.form.get("birth_date", default=None)

            try:
                birth_date = None if birth_date_str is None \
                    else datetime.datetime.strptime(birth_date_str, "%d/%m/%Y").date()
            except (TypeError, ValueError):
                return format_exception_message(
                    exception="Birth date must be provided as %d/%m/%Y"
                ), 400

            salary = request.form.get("salary", default=None)
            if salary and not request.form['salary'].isnumeric():
                return format_exception_message(exception="Salary must be numeric"), 400
            salary = request.form.get("salary", default=None)
            salary = None if salary is None else int(salary)

            updated_emp = EmployeeService.update_employee(
                employee=emp, name=name, department=department,
                job=job, birth_date=birth_date, salary=salary
            )

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400
        return updated_emp.to_dict(), 202

    @staticmethod
    def put(emp_id):
        """
        Put request handler, for editing an employee.
        If a parameter is None, it is set as None for the employee.
        @param emp_id: id of the employee to update
        @return: edited employee as a dictionary or 404 error if employee does not exist
        """
        emp = EmployeeService.get_employee_by_id(emp_id=emp_id)
        name = request.form.get("name", default="")
        department_id = request.form.get("department_id", default="")
        department = DepartmentService.get_department_by_id(department_id)
        job = request.form.get("job", default="")
        birth_date_str = request.form.get("birth_date", default="")
        birth_date = datetime.datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        if not request.form['salary'].isnumeric():
            return format_exception_message(exception="Salary must be numeric"), 400
        salary = request.form.get("salary", default="")
        salary = "" if salary == "" else int(salary)

        try:
            updated_emp = EmployeeService.update_employee(
                employee=emp, name=name, department=department,
                job=job, birth_date=birth_date, salary=salary
            )

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400

        return updated_emp.to_dict(), 202

    @staticmethod
    def delete(emp_id):
        """
        Delete request handler.
        @param emp_id: id of the employee to delete
        """
        emp = EmployeeService.get_employee_by_id(emp_id=emp_id)
        EmployeeService.delete_employee(employee=emp)


