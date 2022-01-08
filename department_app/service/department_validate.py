"""
Module for validating incoming information of a department.
"""

from department_app.database.constraints import DepartmentConstraints


class DepartmentFieldValidations:
    """
    Class which contains methods for validating departments' fields.
    """

    @staticmethod
    def validate_name(name, can_be_none=False):
        """
        Validates name of a department.
        If a field is not correct, an exception is raised.
        @param can_be_none: is name required to be not None
        @param name: name to validate
        """
        if name is None and can_be_none:
            return
        if not isinstance(name, str):
            raise TypeError("Provide department's name as a string")
        if not name:
            raise ValueError("Name is not provided")
        if len(name) > DepartmentConstraints.NAME_MAX_LEN:
            raise ValueError(
                f"Maximum length of the department's name is {DepartmentConstraints.NAME_MAX_LEN}"
            )

    @staticmethod
    def validate_description(description, can_be_none=False):
        """
        Validates department of a department.
        If a field is not correct, an exception is raised.
        @param can_be_none: can description be None
        @param description: department to validate
        """
        if description is None and can_be_none:
            return
        if not isinstance(description, str):
            raise TypeError("Provide department's description as a string")
        if len(description) > DepartmentConstraints.DESCRIPTION_MAX_LEN:
            raise ValueError(
                f"Maximum length of the department's description is "
                f"{DepartmentConstraints.DESCRIPTION_MAX_LEN}"
            )
