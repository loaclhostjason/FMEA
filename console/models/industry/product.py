# coding: utf-8
from ..base import *
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declared_attr


class ProductMixin:
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(12))

    company_name = db.Column(db.String(32), nullable=False)
    project_location = db.Column(db.String(68))
    consumer = db.Column(db.String(68))

    version = db.Column(db.String(68))
    name = db.Column(db.String(68), index=True, nullable=False)

    start_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)

    func_teams = db.Column(db.String(2000))
    fmea_id = db.Column(db.String(20))
    design_resp = db.Column(db.String(128))
