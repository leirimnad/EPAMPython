"""
Module that contains a web view function for the index page of the app.
"""
from flask import render_template
from .web_app import web_app


@web_app.route('/')
def index():
    """
    View for displaying the index page of the app.
    @return: rendered template of the index page of the app
    """
    return render_template("index.html")
