from datetime import datetime
from ..ext import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    """docstring for User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    _name = db.Column(db.String(64), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    website = db.Column(db.String(100))
    resgitered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    display_name = db.Column(db.String(64))

    # def __init__(self, name, password, email):
    #     self.name = name
    #     self._name = self.name.lower()
    #     self.password = password
    #     self.email = email
    #     self.display_name = name

    def __str__(self):
        return self.name


    def is_active(self):
        return self.status

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def verify_email(self, email):
        return check_password_hash(self.email, email)

    @staticmethod
    def authenticate(name, password):
        pw = 'Password Wrong'
        uw = 'Username Wrong'
        user = User.query.filter(db.or_(User.name == name)).first()
        if isinstance(user, User):
            if user.verify_password(password):
                return ("success", user)
            return (pw, None)
        return (uw, None)

    def _get_password(self):
        return self._password_hash

    def _set_password(self, password):
        self._password_hash = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=8)

    password = db.synonym('_password_hash', descriptor=property(
        _get_password, _set_password))

    def create_user(self, name, password, email):
        self.name = name
        self._name = self.name.lower()
        self.password = password
        self.email = email
        self.display_name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

