"""
Module that starts an app, connects to the database
"""

from flask import Flask
from flask_migrate import Migrate
from department_app.database import db, configure_app_env
from department_app.rest import api

app = Flask(__name__, static_url_path='/department_app/static/')

configure_app_env(app=app)
db.init_app(app=app)
api.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
