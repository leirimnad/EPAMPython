"""
Includes service class for working with departments.
"""
from uuid import uuid4

from department_app.models import Department
from department_app.database import db
from department_app.database.constraints import DepartmentConstraints


class DepartmentService:
    """
    Contains functions for working with departments through a database.
    """

    @staticmethod
    def get_department_by_id(dep_id) -> Department:
        """
        Used to get a department instance using its id.
        @param dep_id: id of the department to get
        @return: Department instance or 404 error if department with the needed id does not exist
        """
        return Department.query.get_or_404(dep_id)

    @staticmethod
    def get_all_departments() -> list:
        """
        Used to get a list of all the departments.
        @return: a list of Department instances
        """
        return Department.query.all()

    @staticmethod
    def create_department(name: str, description: str) -> Department:
        """
        Used to create and save a new department.
        @param name: department's name
        @param description: department's description
        @return: created department instance
        """

        if not isinstance(name, str) or not isinstance(description, str):
            raise TypeError("To create a department, provide name and description as strings.")
        if not name:
            raise ValueError("Name of the department is empty")
        if len(name) > DepartmentConstraints.NAME_MAX_LEN:
            raise ValueError(
                f"Maximum length of department name is {DepartmentConstraints.NAME_MAX_LEN}"
            )
        if len(description) > DepartmentConstraints.DESCRIPTION_MAX_LEN:
            raise ValueError(
                f"Maximum length of department description is {DepartmentConstraints.DESCRIPTION_MAX_LEN}"
            )

        dep = Department(id=uuid4(), name=name, description=description)
        db.session.add(dep)
        db.session.commit()
        return dep

    @staticmethod
    def update_department(department, name=None, description=None) -> Department:
        """
        Used to update department's information.
        @param department: department instance to update
        @param name: department's new name (optional)
        @param description: department's new description (optional)
        @return updated department instance
        """

        if name is not None:
            if not isinstance(name, str):
                raise TypeError("Provide name as a string.")
            if name == "":
                raise TypeError("Name of the department is empty")
            if len(name) > DepartmentConstraints.NAME_MAX_LEN:
                raise ValueError(
                    f"Maximum length of department name is {DepartmentConstraints.NAME_MAX_LEN}"
                )
            department.name = name

        if description is not None:
            if not isinstance(description, str):
                raise TypeError("Provide description as a string.")
            if len(description) > DepartmentConstraints.DESCRIPTION_MAX_LEN:
                raise ValueError(
                    f"Maximum length of department description is "
                    f"{DepartmentConstraints.DESCRIPTION_MAX_LEN}"
                )

            department.description = description

        db.session.commit()
        return department

    @staticmethod
    def delete_department(department):
        """
        Used to delete a department from the database.
        @param department: department to delete
        """
        if not isinstance(department, Department):
            raise TypeError("Wrong data type")
        db.session.delete(department)
        db.session.commit()
