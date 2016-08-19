from ..ext import db

class Comment_Meta(db.Model):
    """docstring for Comment_Meta"""

    __tablename__ = 'comment_meta'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, nullable =False)
    meta_key = db.Column(db.String(225))
    meta_value = db.Column(db.Text)

    def __init__(self,user_id, meta_key, meta_value):
        self.user_id = user_id
        self.meta_key = meta_key
        self.meta_value = meta_value