"""
Module that initializes the REST API.
"""

from flask_restful import Api
from .department_api import DepartmentAPI, DepartmentListAPI

api = Api()
api.add_resource(DepartmentListAPI, '/department/')
api.add_resource(DepartmentAPI, '/department/<string:dep_id>')
