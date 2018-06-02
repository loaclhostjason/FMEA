# coding: utf-8
from ..base import *
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


class HelpFilesMixin:
    __tablename__ = 'help_files'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    time = db.Column(db.DateTime, default=datetime.now)
    file = db.Column(db.String(100))
    file_name = db.Column(db.String(100))

    type = db.Column(db.String(12), default='doc')

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    @declared_attr
    def user(cls):
        return db.relationship('User', backref=backref("help_docs", cascade="all, delete-orphan"))


class HelpFiles(HelpFilesMixin, db.Model):
    pass
