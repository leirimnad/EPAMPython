"""
Module that starts an app.
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='/department_app/static/')

DB_USER = os.environ.get("MYSQL_DB_USER")
DB_PASSWORD = os.environ.get("MYSQL_DB_PASSWORD")
DB_HOST = os.environ.get("MYSQL_DB_HOST")
DB_DATABASE = os.environ.get("MYSQL_DB_DATABASE")

app.config["SQLALCHEMY_DATABASE_URI"] = \
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()
