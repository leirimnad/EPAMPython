"""
This module contains a description of a Department model.
"""
from department_app import db


class Department(db.Model):
    """
    Model describing a department.
    """
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=True)

    def __repr__(self):
        return f'<Department {self.id}>'
