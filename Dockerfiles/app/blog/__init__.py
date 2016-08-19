# -*- coding: utf-8 -*-
from .core.app import App
from .ext import configure_extension
from .config import config

main = None

def create_app_base(config_name='default', main_instance=None, **settings):
    app = App(__name__)
    app.config.from_object(config[config_name])
    return app

def create_app(config_name='default', main_instance=None, **settings):
	app = create_app_base(config_name=config_name, main_instance=main_instance, **settings)
	configure_extension(app, main_instance or main )
	return app

def create_celery_app(app=None):
	pass

web=create_app(config_name='produce')
@web.route('/')
def function():
	return 'hello'
