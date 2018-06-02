# coding: utf-8
from ..base import *


class ContactWayMixin:
    __tablename__ = 'contact_way'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(16))
    fax = db.Column(db.String(32))


class ContactWay(ContactWayMixin, db.Model):
    pass