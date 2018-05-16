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

    @classmethod
    def set_base_relation(cls, data):
        d = {
            'name': data.get('name'),
            'parent_id': data.get('parent_id'),
            'product_id': data.get('product_id'),
        }
        r = cls(**d)
        db.session.add(r)
        return
