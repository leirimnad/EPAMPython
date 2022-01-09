"""
Module that defines the REST API for the Employee model.
"""

from flask import request
from flask_restful import Resource
from sqlalchemy import exc as sqlalchemy_err

from department_app.service import EmployeeService
from .utils import format_exception_message, employee_dict_from_http_dict, log_unhandled_exception


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

        try:
            cleaned_data = employee_dict_from_http_dict(request.form, required=True)
            new_emp = EmployeeService.create_employee(**cleaned_data)

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400
        except Exception as exc:
            log_unhandled_exception(exc)
            return format_exception_message(), 500

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
            cleaned_data = employee_dict_from_http_dict(
                request.form, required=False, exclude_keys=["employee"]
            )
            updated_emp = EmployeeService.update_employee(employee=emp, **cleaned_data)
        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400
        except Exception as exc:
            log_unhandled_exception(exc)
            return format_exception_message(), 500

        return updated_emp.to_dict(), 202

    @staticmethod
    def put(emp_id):
        """
        Put request handler, for editing an employee.
        If a parameter is None, the request is rejected.
        @param emp_id: id of the employee to update
        @return: edited employee as a dictionary or 404 error if employee does not exist
        """
        emp = EmployeeService.get_employee_by_id(emp_id=emp_id)

        try:
            cleaned_data = employee_dict_from_http_dict(
                request.form, required=True, exclude_keys=["employee"]
            )
            updated_emp = EmployeeService.update_employee(employee=emp, **cleaned_data)
        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400
        except Exception as exc:
            log_unhandled_exception(exc)
            return format_exception_message(), 500

        return updated_emp.to_dict(), 202

    @staticmethod
    def delete(emp_id):
        """
        Delete request handler.
        @param emp_id: id of the employee to delete
        """
        emp = EmployeeService.get_employee_by_id(emp_id=emp_id)
        EmployeeService.delete_employee(employee=emp)
