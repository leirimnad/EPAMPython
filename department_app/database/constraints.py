"""
Classes DepartmentConstraints and EmployeeConstraints define max length constants for fields.
"""
# pylint:disable=too-few-public-methods


class DepartmentConstraints:
    """
    Constraints for department-related values.
    """
    NAME_MAX_LEN = 80
    DESCRIPTION_MAX_LEN = 300


class EmployeeConstraints:
    """
    Constraints for employee-related values.
    """
    NAME_MAX_LEN = 80
    JOB_MAX_LEN = 100
