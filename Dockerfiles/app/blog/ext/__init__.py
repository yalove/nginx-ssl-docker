# -*- coding: utf-8 -*-

from . import (before_request,
			   error_handlers,
			   cache,
			   db,
			   login,
			   toolbar,
			   views
			   )
from ..app import configure_views

def configure_extension(app, admin):
	before_request.configure(app)
	error_handlers.configure(app)
	cache.configure(app)
	db.configure(app)
	login.configure(app)
	toolbar.configure(app)
	configure_views(app)
	views.configure_static(app)
	return app
	