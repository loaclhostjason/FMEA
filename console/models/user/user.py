from ..base import *
from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declared_attr


class UserBaseMixin:
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True)
    display_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    login_ip = db.Column(db.String(32))
    login_time = db.Column(db.DateTime())
    register_time = db.Column(db.DateTime(), default=datetime.now)

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime)

    role = db.Column(db.String(16))


class User(UserBaseMixin, db.Model):
    pass
