import datetime

from department_app.rest import utils
from testbase import TestBase


class TestOther(TestBase):

    def test_format_exception(self):
        self.assertTrue("Bruh" in utils.format_exception_message("Bruh")["message"])
        self.assertTrue("Bruh error" in utils.format_exception_message(ValueError("Bruh error"))["message"])

    def test_parse_date(self):
        self.assertEqual(datetime.date(2020, 2, 1), utils.parse_date("2020-02-01"))
        self.assertEqual(datetime.date(1990, 1, 11), utils.parse_date("11/01/1990"))
        with self.assertRaises(Exception):
            utils.parse_date("11/31/1990")
        with self.assertRaises(ValueError):
            utils.parse_date("01.01.1990")
