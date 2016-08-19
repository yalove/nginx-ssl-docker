# coding: utf-8
from flask_login import current_user
from flask import g

def configure(app):
    @app.before_first_request
    def initialize():
        from .db import db
        db.create_all()
        app.logger.info("Called only once, when the first request comes in")

    @app.before_request
    def before_request():
        g.user = current_user

