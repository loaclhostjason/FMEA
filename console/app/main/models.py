# coding: utf-8

from models.industry import ProductMixin
from models.industry import ProductRelationMixin
from models.industry import AttrMixin
from models.industry import FuncRelationMixin
from models.industry import FailureRelationMixin

from .. import db
from ..base import Tool, Check


class Product(ProductMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)


class ProductRelation(ProductRelationMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(ProductRelation, self).__init__(*args, **kwargs)

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

        level2 = cls.query.filter(cls.level != 1, cls.level != 0).all()
        if not level2:
            return
        for lv2 in level2:
            parent = cls.query.get_or_404(lv2.parent_id)
            lv2.name_number_set = parent.name_number
            db.session.add(lv2)
        return

    @classmethod
    def add_product_relation(cls, data, content):
        level = data['level']

        len_level = cls.query.filter(cls.level == int(level)).order_by(cls.timestamp.desc(), cls.id.desc()).first()
        start_index = len_level.number + 1 if len_level else 1

        result = []
        for index, con in enumerate(content.split('\r\n'), start=start_index):
            data['name'] = con
            data['number'] = index
            result.append(cls(**data))
        db.session.add_all(result)
        db.session.commit()

        cls.update_name_number()
        return start_index


class Attr(AttrMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(Attr, self).__init__(*args, **kwargs)

    @classmethod
    def edit(cls, form_data, attr):
        Check.update_model(attr, form_data)
        db.session.add(attr)
        return

    @classmethod
    def create_edit_extra(cls, form_data, attr):
        if not attr:
            attr = cls(**form_data)
            db.session.add(attr)
            return

        Check.update_model(attr, form_data)
        db.session.add(attr)
        return

    @classmethod
    def init_attr(cls):
        r = [
            {'name': '结构树节点-0', 'level': 0, 'type': 'structure'},
            {'name': '结构树节点-1', 'level': 1, 'type': 'structure'},
            {'name': '结构树节点-2', 'level': 2, 'type': 'structure'},
            {'name': '结构树节点-3', 'level': 3, 'type': 'structure'},
            {'name': '功能树节点', 'level': None, 'type': 'func'},
            {'name': '失效树节点', 'level': None, 'type': 'failure'},
        ]
        attr = Attr.query.all()
        if attr:
            return
        result = []
        for info in r:
            new_attr = cls(**info)
            result.append(new_attr)
        db.session.add_all(result)
        db.session.commit()
        return


class FuncRelation(FuncRelationMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(FuncRelation, self).__init__(*args, **kwargs)

    @staticmethod
    def update_name_number(parent_id, number):
        parduct_relation = ProductRelation.query.filter_by(id=parent_id).first()
        if not parduct_relation:
            func_relation = FuncRelation.query.filter(FuncRelation.product_id == FuncRelation.product_relation_id).all()
            return '%s-FU%d' % (0, len(func_relation) + 1)

        return '%s-FU%d' % (parduct_relation.name_number, number)

    @classmethod
    def add_func_relation(cls, data, content):
        if not data['parent_id']:
            return

        data['product_relation_id'] = int(data['parent_id'])
        try:
            del data['parent_id']
            del data['level']
        except Exception:
            pass

        content = content.split('\r\n')
        result = []
        for index, con in enumerate(content, start=1):
            data['name'] = con
            data['number'] = index
            data['name_number'] = cls.update_name_number(data['product_relation_id'], index)
            result.append(cls(**data))
        db.session.add_all(result)
        db.session.commit()
        return data['product_relation_id']


class FailureRelation(FailureRelationMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(FailureRelation, self).__init__(*args, **kwargs)

    @staticmethod
    def update_name_number(parent_id, number):
        func_relation = FuncRelation.query.get_or_404(parent_id)
        if not func_relation:
            return

        return '%s-FA%d' % (func_relation.name_number, number)

    @classmethod
    def add_fail_relation(cls, data, content):
        if not data['parent_id']:
            return

        data['func_relation_id'] = int(data['parent_id'])
        try:
            del data['parent_id']
            del data['level']
        except Exception:
            pass

        result = []
        for index, con in enumerate(content.split('\r\n'), start=1):
            data['name'] = con
            data['number'] = index
            data['name_number'] = cls.update_name_number(data['func_relation_id'], index)
            result.append(cls(**data))
        db.session.add_all(result)
        db.session.commit()
        return data['func_relation_id']
