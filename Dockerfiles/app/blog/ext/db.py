# coding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure(app):
	db.init_app(app)
	db.app = app
