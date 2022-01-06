"""
Module that initializes the REST API.
"""

from flask_restful import Api
from .department_api import DepartmentAPI, DepartmentListAPI
from .employee_api import EmployeeAPI, EmployeeListAPI

api = Api()
api.add_resource(DepartmentListAPI, '/department/')
api.add_resource(DepartmentAPI, '/department/<string:dep_id>')

api.add_resource(EmployeeListAPI, '/employee/')
api.add_resource(EmployeeAPI, '/employee/<string:emp_id>')
