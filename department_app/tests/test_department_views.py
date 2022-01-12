from uuid import uuid4

from testbase import TestBase, decode_escapes
from department_app.models import Department


class TestDepartmentViews(TestBase):

    def test_get_departments(self):
        response = self.client.get("/department/")
        self.assertEqual(response.status_code, 200)
        data = decode_escapes(response.get_data(as_text=True))
        self.assertTrue(len(data) > 1)

    def test_create_department(self):
        response = self.client.post(f"/department/add")
        self.assertEqual(response.status_code, 200)
        data = decode_escapes(response.get_data(as_text=True))
        self.assertTrue(len(data) > 1)

    def test_create_department_no_name(self):
        response = self.client.post(f"/department/add")
        data = decode_escapes(response.get_data(as_text=True))
        self.assertTrue("name" in data.lower())

    def test_create_department_empty_name(self):
        response = self.client.post(f"/department/add", data=dict(name="", description="Desc"))
        data = decode_escapes(response.get_data(as_text=True))
        self.assertTrue("name" in data.lower())

    def test_create_department_empty_description(self):
        response = self.client.post(f"/department/add", data=dict(name=uuid4(), description=""))
        self.assertTrue(200 <= response.status_code < 400)

    def test_delete_department(self):
        with self.app.app_context():
            dep = Department.query.first()
        response = self.client.get(f"/department/{dep.id}/delete")
        self.assertTrue(200 <= response.status_code < 400)
        with self.app.app_context():
            self.assertIsNone(Department.query.get(dep.id))

    def test_delete_department_that_not_exists(self):
        response = self.client.get(f"/department/{uuid4()}/delete")
        self.assertTrue(response.status_code >= 400)
