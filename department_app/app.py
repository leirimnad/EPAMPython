"""
Module that starts an app, connects to the database
"""
import logging
import sys

from flask import Flask
from flask_migrate import Migrate
from department_app.database import db, configure_app_env
from department_app.rest import api
from department_app.views import web_app

app = Flask(__name__, static_url_path='/department_app/static/')
app.register_blueprint(web_app)

@app.route('/s')
def bruh():
    return "<h1>Bruhs</h1>"

configure_app_env(app=app)
db.init_app(app=app)
api.init_app(app)
migrate = Migrate(app, db)
logging.basicConfig(
    filename='department_app_logs.log',
    level=logging.WARNING,
    format='%(levelname)s (%(asctime)s): %(message)s',
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


