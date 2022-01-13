"""
Module which creates the 'web_app' Blueprint.
"""
from flask import Blueprint

web_app = Blueprint('web_app', __name__, template_folder='templates')
