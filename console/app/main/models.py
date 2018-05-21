# coding: utf-8

from models.industry import ProductMixin
from models.industry import ProductChildRelationMixin
from models.industry import AttrMixin

from .. import db


class Product(ProductMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Product: {}>'.format(self.id)


class ProductChildRelation(ProductChildRelationMixin, db.Model):
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

    @property
    def name_number_set(self):
        raise AttributeError('no getter name_number_set')

    @name_number_set.setter
    def name_number_set(self, parent_name_number=None):
        if not self.level or self.level not in [1, 2, 3]:
            return
        if self.level == 1:
            self.name_number = '{}'.format(self.number)
            return

        if not parent_name_number:
            raise ValueError('no parent_name_number!!')

        if self.level == 2:
            self.name_number = '{}.{}'.format(parent_name_number, self.number)
        if self.level == 3:
            self.name_number = '{}.{}'.format(parent_name_number, self.number)
        return

    @classmethod
    def update_name_number(cls):
        level1 = cls.query.filter(cls.level == 1).all()
        if not level1:
            return

        for le in level1:
            le.name_number_set = None
            db.session.add(le)

        level2 = cls.query.filter(cls.level != 1).all()
        if not level2:
            return
        for lv2 in level2:
            parent = cls.query.get_or_404(lv2.parent_id)
            lv2.name_number_set = parent.name_number
            db.session.add(lv2)
        return


class Attr(AttrMixin, db.Model):
    pass
