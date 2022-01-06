import unittest
import uuid

from testbase import TestBase, DEP_COUNT
from werkzeug import exceptions
from sqlalchemy import exc

from department_app.service.department_service import DepartmentService, Department
from department_app.database import db


class TestDepartmentService(TestBase):

    def test_create_department(self):
        with self.app.app_context():
            count = Department.query.count()
            DepartmentService.create_department("Random department name", "Desc")
            self.assertEqual(Department.query.count(), count+1)

            with self.assertRaises(exc.IntegrityError):
                DepartmentService.create_department("Random department name", "Yep, there are two now")

            db.session.rollback()
            self.assertEqual(Department.query.count(), count+1)

    def test_get_department_by_id(self):
        with self.app.app_context():
            dep = Department.query.first()
            dep_found = DepartmentService.get_department_by_id(dep_id=dep.id)
            self.assertIsNotNone(dep_found)
            self.assertEqual(dep_found.name, dep.name)

    def test_get_department_by_id_random(self):
        with self.app.app_context():
            with self.assertRaises(exceptions.NotFound):
                DepartmentService.get_department_by_id(str(uuid.uuid4()))

    def test_get_all_departments(self):
        with self.app.app_context():
            deps = DepartmentService.get_all_departments()
            self.assertEqual(len(deps), DEP_COUNT)

    def test_update_department_empty(self):
        with self.app.app_context():
            dep = Department.query.first()
            name, desc = dep.name, dep.description
            DepartmentService.update_department(dep)
            self.assertEqual(name, dep.name)
            self.assertEqual(desc, dep.description)

    def test_update_department_name(self):
        with self.app.app_context():
            dep = Department.query.first()
            name, desc = dep.name, dep.description
            new_name = str(uuid.uuid4())
            DepartmentService.update_department(dep, name=new_name)
            self.assertEqual(dep.name, new_name)
            self.assertEqual(dep.description, desc)

    def test_update_department_description(self):
        with self.app.app_context():
            dep = Department.query.first()
            name, desc = dep.name, dep.description
            new_desc = str(uuid.uuid4())
            DepartmentService.update_department(dep, description=new_desc)
            self.assertEqual(dep.name, name)
            self.assertEqual(dep.description, new_desc)

    def test_update_department_name_and_description(self):
        with self.app.app_context():
            dep = Department.query.first()
            new_name = str(uuid.uuid4())
            new_desc = str(uuid.uuid4())
            DepartmentService.update_department(dep, name=new_name, description=new_desc)
            self.assertEqual(dep.name, new_name)
            self.assertEqual(dep.description, new_desc)

    def test_delete_department(self):
        with self.app.app_context():
            dep = Department.query.first()
            DepartmentService.delete_department(dep)
            self.assertIsNone(Department.query.get(dep.id))


if __name__ == "__main__":
    unittest.main()
