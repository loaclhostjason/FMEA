# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import request, current_app
from flask_login import current_user
from datetime import datetime
from . import db, login_manager

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from models.user.user import UserBaseMixin


class User(UserBaseMixin, UserMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def bool_password(self):
        return bool(self.password_hash)

    def is_admin(self):
        return bool(self.username == 'admin')

    @classmethod
    def update_time_ip(cls):
        user = cls.query.filter(cls.username == current_user.username).first_or_404()
        user.login_time = datetime.now()
        user.login_ip = request.remote_addr
        db.session.add(user)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        self.confirmed_on = datetime.now()
        db.session.add(self)
        return True

    @staticmethod
    def insert_admin():
        u = {
            'username': '超级管理员',
            'email': 'admin@qq.com',
            'password': '123',
            'role': 'admin',
            'confirmed': True,
            'confirmed_on': datetime.now(),
        }
        old = User.query.filter_by(username=u['username']).first()
        if not old:
            db.session.add(User(**u))
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
