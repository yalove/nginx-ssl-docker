from ..ext import db
from datetime import datetime

class Comment(db.Model):
    """docstring for Comment"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    topic_id = db.Column(db.Integer, nullable = False)
    author = db.Column(db.String(64), nullable = False)
    author_email = db.Column(db.String(100), nullable = False)
    author_url = db.Column(db.String(200))
    author_ip  = db.Column(db.String(100))
    date = db.Column(db.DateTime, default = datetime.utcnow())
    markdown = db.Column(db.Text)
    html = db.Column(db.Text)
    status = db.Column(db.String(20))
    agent = db.Column(db.String(225))
    type = db.Column(db.String(20))
    parent = db.Column(db.Integer)
    user_id = db.Column(db.Integer,default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self