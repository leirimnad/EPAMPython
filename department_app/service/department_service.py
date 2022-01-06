"""
Includes service class for working with departments.
"""

from department_app.models import Department


class DepartmentService:
    """
    Contains functions for working with departments through a database.
    """

    @staticmethod
    def get_department_by_id(dep_id):
        """
        Used to get a department instance using its id.
        @param dep_id: id of the department to get
        @return: Department instance or 404 error if department with the needed id does not exist
        """
        return Department.query.get_or_404(dep_id)

    @staticmethod
    def get_all_departments():
        """
        Used to get a list of all the departments.
        @return: a list of Department instances
        """
        return Department.query.all()
