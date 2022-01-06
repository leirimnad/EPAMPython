"""
Module that defines the REST API for the Department model.
"""

from flask_restful import Resource
from department_app.service import DepartmentService


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


class DepartmentAPI(Resource):
    """
    Defines the REST API for a single department query.
    """

    @staticmethod
    def get(dep_id):
        """
        Get request handler.
        @param dep_id: id of the department to get
        @return: departments as a dictionary or 404 error if department does not exist
        """
        dep = DepartmentService.get_department_by_id(dep_id=dep_id)
        return dep.to_dict()
