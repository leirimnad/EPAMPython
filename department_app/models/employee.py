"""
Module that describes the model of an employee.
"""

from sqlalchemy.orm import backref
from department_app.database import db


class Employee(db.Model):
    """
    Model describing an employee.
    """

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    department_id = db.Column(db.String(36), db.ForeignKey("department.id"))
    job = db.Column(db.String(100), unique=False, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    department = db.relationship("Department",
                                 backref=backref("employee", cascade="all,delete"),
                                 lazy=True)

    # pylint: disable=E1101
    def to_dict(self):
        """
        Returns a subscriptable dictionary representing the employee.
        @return: employee dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "department_id": self.department_id,
            "job": self.job,
            "birth_date": self.birth_date.strftime("%d/%m/%Y"),
            "salary": self.salary
        }

    def __repr__(self):
        return f'<Employee {self.id}>'
