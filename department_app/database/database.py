"""
Database module is used to create an SQLAlchemy database instance.
"""

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure_app(app, /, db_user, db_password, db_host, db_database):
    """
    Configures an app's mysql database connection.
    @param app: Flask app instance
    @param db_user: MySQL user
    @param db_password: MySQL password
    @param db_host: MySQL host
    @param db_database: MySQL database
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def configure_app_env(app):
    """
    Configures an app's mysql database connection using environmental variables:
    MYSQL_DB_USER: MySQL user
    MYSQL_DB_PASSWORD: MySQL password
    MYSQL_DB_HOST: MySQL host
    MYSQL_DB_DATABASE: MySQL database
    @param app: Flask app instance
    """
    db_user = os.environ.get("MYSQL_DB_USER")
    db_password = os.environ.get("MYSQL_DB_PASSWORD")
    db_host = os.environ.get("MYSQL_DB_HOST")
    db_database = os.environ.get("MYSQL_DB_DATABASE")

    configure_app(app, db_user, db_password, db_host, db_database)
