import codecs
import re
from string import ascii_lowercase
import random
from uuid import uuid4

from testbase import TestBase, decode_escapes
from department_app.models import Department
from department_app.database.constraints import DepartmentConstraints


class TestDepartmentAPI(TestBase):

    def test_get_departments(self):
        response = self.client.get("/api/department/")
        self.assertEqual(response.status_code, 200)
        data = decode_escapes(response.get_data(as_text=True))
        self.assertTrue(len(data) > 1)

        with self.app.app_context():
            for dep in Department.query.all():
                self.assertTrue(dep.id in data)
                self.assertTrue(dep.name in data)
                self.assertTrue(dep.description in data)

    def test_get_department(self):

        with self.app.app_context():
            dep = Department.query.first()

        response = self.client.get(f"/api/department/{dep.id}")
        data = decode_escapes(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dep.id in data)
        self.assertTrue(dep.name in data)
        self.assertTrue(dep.description in data)

    def test_create_department_no_name(self):
        response = self.client.post(f"/api/department/")
        self.assertTrue(response.status_code >= 400)

    def test_create_department_empty_name(self):
        response = self.client.post(f"/api/department/", data=dict(name="", description="Desc"))
        self.assertTrue(response.status_code >= 400)

    def test_create_department_empty_description(self):
        response = self.client.post(f"/api/department/", data=dict(name=uuid4(), description=""))
        self.assertTrue(200 <= response.status_code < 300)

    def test_create_department_not_unique_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        response = self.client.post(f"/api/department/", data=dict(name=dep.name, description=""))
        self.assertTrue(response.status_code >= 400)

    def test_create_department_not_unique_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        response = self.client.post(f"/api/department/", data=dict(name=uuid4(), description=dep.description))
        self.assertTrue(200 <= response.status_code < 300)

    def test_create_department_long_name(self):
        test_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.NAME_MAX_LEN + 10)]
        )
        response = self.client.post(f"/api/department/", data=dict(name=test_name, description="Desc"))
        self.assertTrue(response.status_code >= 400)

    def test_create_department_long_description(self):
        test_desc = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.DESCRIPTION_MAX_LEN + 10)]
        )
        response = self.client.post(f"/api/department/", data=dict(name=test_desc[:40], description=test_desc))
        self.assertTrue(response.status_code >= 400)

    def test_create_department_long_name_and_description(self):
        test_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.NAME_MAX_LEN + 10)]
        )
        test_desc = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.DESCRIPTION_MAX_LEN + 10)]
        )
        response = self.client.post(f"/api/department/", data=dict(name=test_name, description=test_desc))
        self.assertTrue(response.status_code >= 400)

    def test_patch(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_name = str(uuid4())
        new_desc = str(uuid4())
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(name=new_name, description=new_desc))
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_dep = Department.query.get(dep.id)
        self.assertEqual(new_name, got_dep.name)
        self.assertEqual(new_desc, got_dep.description)

    def test_patch_department_no_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_desc = str(uuid4())
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(description=new_desc))
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_dep = Department.query.get(dep.id)
        self.assertEqual(dep.name, got_dep.name)
        self.assertEqual(new_desc, got_dep.description)

    def test_patch_department_empty_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_desc = str(uuid4())
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(name="", description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_patch_department_empty_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(description=""))
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_dep = Department.query.get(dep.id)
        self.assertEqual(dep.name, got_dep.name)
        self.assertEqual("", got_dep.description)

    def test_patch_department_long_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.NAME_MAX_LEN + 10)]
        )
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(name=new_name))
        self.assertTrue(response.status_code >= 400)

    def test_patch_department_long_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_desc = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.DESCRIPTION_MAX_LEN + 10)]
        )
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_patch_department_long_name_and_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.NAME_MAX_LEN + 10)]
        )
        new_desc = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.DESCRIPTION_MAX_LEN + 10)]
        )
        response = self.client.patch(f"/api/department/{dep.id}", data=dict(name=new_name, description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_patch_department_not_unique_name(self):
        with self.app.app_context():
            deps = Department.query.limit(2).all()

        response = self.client.patch(f"/api/department/{deps[1].id}", data=dict(name=deps[0].name, description=""))
        self.assertTrue(response.status_code >= 400)

    def test_patch_department_not_unique_description(self):
        with self.app.app_context():
            deps = Department.query.limit(2).all()
        response = self.client.patch(f"/api/department/{deps[1].id}",
                                     data=dict(
                                         name=uuid4(),
                                         description=deps[0].description
                                     )
                                     )
        self.assertTrue(200 <= response.status_code < 300)

    def test_put(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_name = str(uuid4())
        new_desc = str(uuid4())
        response = self.client.put(f"/api/department/{dep.id}", data=dict(name=new_name, description=new_desc))
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_dep = Department.query.get(dep.id)
        self.assertEqual(new_name, got_dep.name)
        self.assertEqual(new_desc, got_dep.description)

    def test_put_department_no_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_desc = str(uuid4())
        response = self.client.put(f"/api/department/{dep.id}", data=dict(description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_put_department_empty_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_desc = str(uuid4())
        response = self.client.put(f"/api/department/{dep.id}", data=dict(name="", description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_put_department_empty_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        response = self.client.put(f"/api/department/{dep.id}", data=dict(name=dep.name, description=""))
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            got_dep = Department.query.get(dep.id)
        self.assertEqual(dep.name, got_dep.name)
        self.assertEqual("", got_dep.description)

    def test_put_department_long_name(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.NAME_MAX_LEN + 10)]
        )
        response = self.client.put(f"/api/department/{dep.id}", data=dict(name=new_name, description=uuid4()))
        self.assertTrue(response.status_code >= 400)

    def test_put_department_long_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_desc = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.DESCRIPTION_MAX_LEN + 10)]
        )
        response = self.client.put(f"/api/department/{dep.id}", data=dict(name=uuid4(), description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_put_department_long_name_and_description(self):
        with self.app.app_context():
            dep = Department.query.first()
        new_name = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.NAME_MAX_LEN + 10)]
        )
        new_desc = "".join(
            [random.choice(ascii_lowercase) for _ in range(DepartmentConstraints.DESCRIPTION_MAX_LEN + 10)]
        )
        response = self.client.put(f"/api/department/{dep.id}", data=dict(name=new_name, description=new_desc))
        self.assertTrue(response.status_code >= 400)

    def test_put_department_not_unique_name(self):
        with self.app.app_context():
            deps = Department.query.limit(2).all()
        response = self.client.put(f"/api/department/{deps[1].id}", data=dict(name=deps[0].name, description=""))
        self.assertTrue(response.status_code >= 400)

    def test_put_department_not_unique_description(self):
        with self.app.app_context():
            deps = Department.query.limit(2).all()
        response = self.client.put(f"/api/department/{deps[1].id}",
                                   data=dict(
                                       name=uuid4(),
                                       description=deps[0].description
                                   )
                                   )
        self.assertTrue(200 <= response.status_code < 300)

    def test_delete_department(self):
        with self.app.app_context():
            dep = Department.query.first()
        response = self.client.delete(f"/api/department/{dep.id}")
        self.assertTrue(200 <= response.status_code < 300)
        with self.app.app_context():
            self.assertIsNone(Department.query.get(dep.id))

    def test_delete_department_that_not_exists(self):
        response = self.client.delete(f"/api/department/{uuid4()}")
        self.assertTrue(response.status_code >= 400)
