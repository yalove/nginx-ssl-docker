# coding: utf-8

from flask.ext.cache import Cache

cache = Cache()

def configure(app):
	cache.init_app(app)