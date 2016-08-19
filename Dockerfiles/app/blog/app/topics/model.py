from datetime import datetime
from flask import current_app
from ..ext import db


class Topic(db.Model):
    """docstring for Topic"""

    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable = False)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    date = db.Column(db.DateTime, default = datetime.utcnow())
    modified = db.Column(db.DateTime, default = datetime.utcnow())
    to_ping = db.Column(db.Text)
    pinged = db.Column(db.Text)
    content_filtered = db.Column(db.Text)
    topic_parent = db.Column(db.Integer)
    url = db.Column(db.String(200))
    excerpt = db.Column(db.Text)
    status = db.Column(db.Boolean, default = True)
    comment_status = db.Column(db.Boolean, default = True)
    ping_status = db.Column(db.Boolean, default = True)
    password = db.Column(db.String(64))
    user_id = db.Column(db.Integer)
    comment_count = db.Column(db.Integer,default=0)

    # def __init__(self, user, title, markdown):
    #     self.user_id = user.id
    #     self.name = title
    #     self.title = title
    #     self.markdown = markdown
    #     return self
 
    def create_topic(self, user, title, markdown):
        self.user_id = user.id
        self.name = title
        self.title = title
        self.markdown = markdown
        return self


    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
            current_app.logger.info("have post")
        except Exception, e:
            current_app.logger.exception("something went wrong while  saving a post")
            db.session.rollback()
            return False
        return True