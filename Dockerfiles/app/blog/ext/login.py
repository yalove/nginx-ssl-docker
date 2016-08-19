# coding: utf-8
from flask.ext.login import LoginManager
from flask import current_app

from ..app.users.model import User
from ..app.topics.model import Topic
from ..app.models.comment import Comment


lm = LoginManager()
lm.login_view = 'user.login'
#lm.anonymous_user = Guest

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def configure(app):
	lm.init_app(app)
	app.config['model']={'user':User,'topic':Topic,'comment':Comment}