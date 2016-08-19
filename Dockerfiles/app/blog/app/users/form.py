from flask_login import current_user
from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, SelectField, ValidationError, SubmitField,BooleanField,FileField)
from wtforms.validators import(Length, DataRequired, InputRequired, Email, EqualTo, Optional, URL)

from .model import User
from ..ext import db
from ..ext import CustomForm

class LoginForm(CustomForm):
    name = StringField("username", validators=[DataRequired(message="username")])
    password = PasswordField("password", validators=[DataRequired(message="username")])
    remember_me =BooleanField("remember_me",default=False)

class RegisterForm(CustomForm):
    username = StringField("User", validators=[DataRequired(message="username")])
    email = StringField("email",validators=[DataRequired(message="username"),Email(message="invalidate_email")] )
    password = PasswordField("password",validators=[InputRequired()])
    def validate_username(self, field):
        user = User.query.filter_by(_name= field.data.lower()).first()
        if user:
            raise ValidationError("already used")
    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError("already used")
    def save(self):
        user= User(name=self.username.data,
                    email= self.email.data,
                    _name=self.username.data.lower(),
                    password=self.password.data,
            )
        return user.save()

class EditProfileForm(CustomForm):
    website=StringField("Website", validators=[Optional(),URL()])
    avater= StringField("Avatar", validators=[Optional()])
    signature=StringField("Signature",validators=[Optional()])

    # def validate_avatar(self,field):
    #     if field.data is not None:
    #         error , status = check_image(field.data)
    #         if error is not None:
    #             raise ValidationError(error)
    #         return status


#class RegisterRecaptchaForm(RegisterForm):



#class ReauthForm(Form):



#class ForgotPasswordForm(Form):


class ChangePasswordForm(CustomForm):
    password = PasswordField("Your Password",validators=[
        DataRequired()])
    new_password = PasswordField('New Password',validators=[
        DataRequired()])


class UploadForm(CustomForm):
    fileload = FileField('Your photo')

