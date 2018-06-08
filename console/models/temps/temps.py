# coding: utf-8
from ..base import *
from datetime import datetime


class TempsMixin:
    __tablename__ = 'temps'
    id = db.Column(db.Integer, primary_key=True)

    # 名称 and 等级
    name = db.Column(db.String(32))
    level = db.Column(db.Integer, index=True, default=0)
    number = db.Column(db.Integer, default=1)
    name_number = db.Column(db.String(32), index=True)

    timestamp = db.Column(db.DateTime, default=datetime.now)

    parent_id = db.Column(db.Integer, index=True)


class Temps(TempsMixin, db.Model):
    pass
