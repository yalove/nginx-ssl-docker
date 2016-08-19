from ..ext import db
from flask_login import current_user
from flask import flash
class User_Meta(db.Model):
    """docstring for User_Meta"""

    __tablename__ = 'user_meta'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, nullable =False)
    meta_key = db.Column(db.String(225))
    meta_value = db.Column(db.Text)


    def set(self,user_id,meta_key,meta_value):

        self.user_id = user_id 
        self.meta_key = meta_key
        self.meta_value = meta_value
        db.session.add(self)
        db.session.commit()
        return self