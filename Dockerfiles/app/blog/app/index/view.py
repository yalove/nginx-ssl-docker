import datetime
from flask import Blueprint, render_template, current_app
from ..users.model import User
from ..topics.model import Topic
from ..ext import cache
from ..ext import db

def set_relation_model(instance, relate_model, attr,attr1):
    if hasattr(instance,attr):
        user = db.session.query(relate_model).get(getattr(instance, attr))
        setattr(instance,attr1, user)


index = Blueprint('index', __name__)


@index.route("/", methods = ['GET', 'POST'])
@index.route("/<int:page>", methods = ['GET', 'POST'])
@cache.cached(timeout=50)
def indexs(page=1):
	POSTS_PER_PAGE = current_app.config.get('POSTS_PER_PAGE') or 5
	paginate = Topic.query.paginate(int(page), POSTS_PER_PAGE, False)
	for item in paginate.items:
		set_relation_model(item, User, 'user_id', 'user')
	return render_template('index.html',paginate = paginate)
