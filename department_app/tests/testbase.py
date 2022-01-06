import unittest

from department_app.app import app
from department_app.database import db, configure_app_env


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app
        app.config['TESTING'] = True
        configure_app_env(app)
        db.init_app(app=app)
        with app.app_context():
            db.create_all()


    @classmethod
    def tearDownClass(cls) -> None:
        ...
