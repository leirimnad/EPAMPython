from flask import Blueprint

web_app = Blueprint('web_app', __name__, template_folder='templates')

from . import department_views, index
