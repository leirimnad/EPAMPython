import unittest

from department_app.app import app
from department_app.database import db, configure_app_env
from department_app.help.populate import populate_database, DEP_COUNT, EMP_COUNT


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = app.test_client()
        self.app = app
        app.config['TESTING'] = True
        configure_app_env(app)
        db.init_app(app=app)
        populate_database(app)

    def tearDown(self) -> None:
        with app.app_context():
            db.session.close()
            db.drop_all()

    @classmethod
    def tearDownClass(cls) -> None:
        ...
