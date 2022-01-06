from testbase import TestBase
from department_app.models import Department


class TestDepartmentAPI(TestBase):

    def test_get_departments(self):
        response = self.client.get("/department/")
        self.assertEqual(response.status_code, 200)
        data = str(response.data)
        self.assertTrue(len(data) > 1)

        with self.app.app_context():
            for dep in Department.query.all():
                self.assertTrue(dep.id in data)
                self.assertTrue(dep.name in data)
                self.assertTrue(dep.description in data)

    def test_get_department(self):

        with self.app.app_context():
            dep = Department.query.first()

        response = self.client.get(f"/department/{dep.id}")
        data = str(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dep.id in data)
        self.assertTrue(dep.name in data)
        self.assertTrue(dep.description in data)




