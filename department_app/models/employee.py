"""
Module that describes the model of an employee.
"""

from department_app.database import db


class Employee(db.Model):
    """
    Model describing an employee.
    """

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    department_id = db.Column(db.String(36), db.ForeignKey("department.id"))
    department = db.relationship("Department", backref="employee", lazy=True)
    job = db.Column(db.String(100), unique=False, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)

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
            "birth_date": self.birth_date,
            "salary": self.salary
        }

    def __repr__(self):
        return f'<Employee {self.id}>'
