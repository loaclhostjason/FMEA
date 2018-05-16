# coding: utf-8

from models.industry import ProductMixin
from models.industry import AnalysisMixin

from .. import db
from ..models import BaseModelFunc


class Product(ProductMixin, BaseModelFunc, db.Model):
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Product: {}>'.format(self.id)


class ProductChildRelation(AnalysisMixin, BaseModelFunc, db.Model):
    def __init__(self, *args, **kwargs):
        super(ProductChildRelation, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<ProductChildRelation: {}>'.format(self.id)
