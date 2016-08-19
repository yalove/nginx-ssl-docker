# -*- coding: utf-8 -*-
from .users.view import user
from .topics.view import topic
from .index.view import index
from .weixin.view import weixin
from .dashboard.dashview import Dash, DashPanel
from .upload.view import upload
from .ext import db

from .users.model import User
from .topics.model import Topic

views = [user, topic, index, upload, weixin]

models = [User, Topic]


def configure_views(app):
    for view in views:
        app.register_blueprint(view)

    dash = Dash(app)
    user_list = ['id','name','email','website','resgitered','status','display_name']
    topic_list =['id','title','date','status','user','markdown', 'html']
    for model in models:
        if model==User:
            dash.register_model(model,db.session,user_list)
        elif model == Topic:
            dash.register_model(model, db.session,topic_list)
        else:
            dash.register_model(model, db.session)

    dash.setup()