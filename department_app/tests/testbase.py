import codecs
import re
import unittest

from department_app.app import app
from department_app.database import db, configure_app_env
from department_app.help.populate import populate_database


def decode_escapes(s):
    ESCAPE_SEQUENCE_RE = re.compile(r'''
                ( \\U........      # 8-digit hex escapes
                | \\u....          # 4-digit hex escapes
                | \\x..            # 2-digit hex escapes
                | \\[0-7]{1,3}     # Octal escapes
                | \\N\{[^}]+\}     # Unicode characters by name
                | \\[\\'"abfnrtv]  # Single-character escapes
                )''', re.UNICODE | re.VERBOSE)

    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


class TestBase(unittest.TestCase):
    DEP_COUNT = 2
    EMP_COUNT = 4

    def setUp(self) -> None:
        self.client = app.test_client()
        self.app = app
        app.config['TESTING'] = True
        configure_app_env(app)
        db.init_app(app=app)
        with app.app_context():
            db.session.rollback()
        populate_database(app, dep_count=self.DEP_COUNT, emp_count=self.EMP_COUNT)

    def tearDown(self) -> None:
        with app.app_context():
            db.session.close()
            db.drop_all()

    @classmethod
    def tearDownClass(cls) -> None:
        ...
