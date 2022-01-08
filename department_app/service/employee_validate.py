"""
Module for validating incoming information of an employee.
"""

from datetime import date
from department_app.database.constraints import EmployeeConstraints


class EmployeeFieldValidations:
    """
    Class which contains methods for validating employees' fields.
    """

    # pylint: disable=too-many-arguments
    @classmethod
    def validate_all(cls, name, department, job, birth_date, salary):
        """
        Validates all fields of an employee.
        If a field is not correct, an exception is raised.
        @param name: name to validate
        @param department: department to validate
        @param job: job to validate
        @param birth_date: birth date to validate
        @param salary: salary to validate
        """
        cls.validate_name(name)
        cls.validate_department(department)
        cls.validate_job(job)
        cls.validate_birth_date(birth_date)
        cls.validate_salary(salary)

    @staticmethod
    def validate_name(name):
        """
        Validates name of an employee.
        If a field is not correct, an exception is raised.
        @param name: name to validate
        """
        if not isinstance(name, str):
            raise TypeError("Provide employee's name as a string")
        if not name:
            raise ValueError("Name is not provided")
        if len(name) > EmployeeConstraints.NAME_MAX_LEN:
            raise ValueError(
                f"Maximum length of the employee's name is {EmployeeConstraints.NAME_MAX_LEN}"
            )

    @staticmethod
    def validate_department(department):
        """
        Validates department of an employee.
        If a field is not correct, an exception is raised.
        @param department: department to validate
        """
        if not department:
            raise ValueError("Department is not provided")

    @staticmethod
    def validate_job(job):
        """
        Validates job of an employee.
        If a field is not correct, an exception is raised.
        @param job: job to validate
        """
        if not isinstance(job, str):
            raise TypeError("Provide employee's job as a string")
        if not job:
            raise ValueError("Job is not provided")
        if len(job) > EmployeeConstraints.JOB_MAX_LEN:
            raise ValueError(
                f"Maximum length of the employee's job is {EmployeeConstraints.JOB_MAX_LEN}"
            )

    @staticmethod
    def validate_birth_date(birth_date):
        """
        Validates birthdate of an employee.
        If a field is not correct, an exception is raised.
        @param birth_date: date to validate
        """
        if not isinstance(birth_date, date):
            raise TypeError("Provide employee's birth date as a date")
        if birth_date > date.today():
            raise ValueError("Employee's date of birth is in the future")

    @staticmethod
    def validate_salary(salary):
        """
        Validates a salary.
        @param salary: salary to validate
        """
        if not isinstance(salary, int):
            raise TypeError("Provide employee's salary as an integer")
        if salary < 0:
            raise ValueError("Employee's salary is negative")
