from flask_login import current_user
from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, SelectField, ValidationError, SubmitField,BooleanField,FileField)
from wtforms.validators import(Length, DataRequired, InputRequired, Email, EqualTo, Optional, URL)

from .model import Topic
from ..ext import db
from ..ext import CustomForm


class TopicForm(CustomForm):
    """docstring for TopicForm"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Article', validators=[DataRequired()])
    submit = SubmitField('submit')

    def validate_title(self, field):
        if Topic.query.filter_by(user_id=current_user.id, name = self.title.data).first() is not None:
            raise ValidationError("You have already posted an article with the same title")