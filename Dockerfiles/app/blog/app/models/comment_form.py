from flask import request
from flask_wtf import Form
from flask_login import current_user
from wtforms import (StringField, PasswordField, TextAreaField,
                     SelectField, ValidationError, SubmitField, BooleanField, FileField)
from wtforms.validators import(
    Length, DataRequired, InputRequired, Email, EqualTo, Optional, URL)

from ..users.model import User
from ..topics.model import Topic
from .comment import Comment
from ..ext import db
from ..ext import CustomForm


class Comment_Form(CustomForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    website = StringField('website')
    content = TextAreaField('comment', validators=[DataRequired()])

    def save(self, topic, user):
        comment = Comment()
        comment.topic_id = topic.id
        comment.author = self.name.data
        comment.author_email = self.email.data
        comment.author_url = self.website.data
        comment.author_ip = request.remote_addr
        comment.markdown = self.content.data
        comment.agent = request.headers.get('User-Agent')
        count = Comment.query.filter_by(topic_id=topic.id).all().__len__()
        topic.comment_count = count + 1
        topic.save()
        return comment.save()


class Comment_User_Form(CustomForm):
    content = TextAreaField('comment', validators=[DataRequired()])

    def save(self, topic, user, parent=0):
        comment = Comment()
        comment.topic_id = topic.id
        comment.author = current_user.name
        comment.author_email = current_user.email
        comment.author_url = current_user.website
        comment.author_ip = request.remote_addr
        comment.user_id = current_user.id
        comment.markdown = self.content.data
        comment.agent = request.headers.get('User-Agent')
        comment.status = "publish"
        comment.parent = parent
        count = Comment.query.filter_by(topic_id=topic.id).all().__len__()
        topic.comment_count = count + 1
        topic.save()
        return comment.save()
