# coding: utf-8

from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension()

def configure(app):
	toolbar.init_app(app)