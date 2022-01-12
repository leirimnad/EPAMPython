"""
Module with web views for the app.
Web views come as a separate Blueprint with 'web_app' name.
The endpoints which mention views from this module may start with 'web_app.'
"""

from . import department_views, employee_views, index
from .web_app import web_app
