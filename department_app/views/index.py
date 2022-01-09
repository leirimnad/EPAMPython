from flask import render_template
from . import web_app


@web_app.route('/')
def index():
    return render_template("index.html")
