import unittest
import uuid

from testbase import TestBase
from werkzeug import exceptions

from department_app.service.department_service import DepartmentService


class TestSample(TestBase):

    def test_get_department_by_id_random(self):
        with self.app.app_context():
            with self.assertRaises(exceptions.NotFound):
                DepartmentService.get_department_by_id(uuid.uuid4())


if __name__ == "__main__":
    unittest.main()
