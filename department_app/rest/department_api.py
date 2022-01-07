"""
Module that defines the REST API for the Department model.
"""

from flask import request
from flask_restful import Resource
from pymysql import err as pymysql_err
from sqlalchemy import exc as sqlalchemy_err

from department_app.service import DepartmentService
from .utils import format_exception_message


class DepartmentListAPI(Resource):
    """
    Defines the REST API for the full list of departments.
    """

    @staticmethod
    def get():
        """
        Get request handler.
        @return: list of departments dictionaries
        """
        deps = DepartmentService.get_all_departments()
        return [dep.to_dict() for dep in deps]

    @staticmethod
    def post():
        """
        Put request handler.
        @return: new department as dictionary, if one was successfully created
        """
        name = request.form['name']
        description = request.form['description']

        try:
            new_dep = DepartmentService.create_department(name=name, description=description)

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400

        return new_dep.to_dict(), 202


class DepartmentAPI(Resource):
    """
    Defines the REST API for a single department query.
    """

    @staticmethod
    def get(dep_id):
        """
        Get request handler.
        @param dep_id: id of the department to get
        @return: department as a dictionary or 404 error if department does not exist
        """
        dep = DepartmentService.get_department_by_id(dep_id=dep_id)
        return dep.to_dict()

    @staticmethod
    def patch(dep_id):
        """
        Patch request handler, for editing a department.
        If a parameter is None, it is not changed in the department.
        @param dep_id: id of the department to update
        @return: edited department as a dictionary or 404 error if department does not exist
        """
        dep = DepartmentService.get_department_by_id(dep_id=dep_id)
        name = request.form.get("name", default=None)
        description = request.form.get("description", default=None)

        try:
            updated_dep = DepartmentService.update_department(department=dep, name=name, description=description)

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400

        return updated_dep.to_dict(), 202

    @staticmethod
    def put(dep_id):
        """
        Put request handler, for editing a department.
        If a parameter is None, it is set as None in the department.
        @param dep_id: id of the department to update
        @return: edited department as a dictionary or 404 error if department does not exist
        """
        dep = DepartmentService.get_department_by_id(dep_id=dep_id)
        name = request.form.get("name", default="")
        description = request.form.get("description", default="")

        try:
            updated_dep = DepartmentService.update_department(department=dep, name=name, description=description)

        except (ValueError, TypeError) as exc:
            return format_exception_message(exception=exc), 400
        except sqlalchemy_err.IntegrityError as exc:
            return format_exception_message(exc.orig), 400

        return updated_dep.to_dict(), 202

    @staticmethod
    def delete(dep_id):
        """
        Delete request handler.
        @param dep_id: id of the department to delete
        """
        dep = DepartmentService.get_department_by_id(dep_id=dep_id)
        DepartmentService.delete_department(department=dep)
