# coding: utf-8
from .. import db
from models.industry.product import AttrContentMixin
import json
from sqlalchemy import or_


class AttrContent(AttrContentMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(AttrContent, self).__init__(*args, **kwargs)

    def get_insert_data(self, data, product_id, type):
        if not data:
            return
        level = data.get('level')
        try:
            del data['level']
        except:
            pass
        d = {
            'level': level,
            'product_id': product_id,
            'real_content': json.dumps(data),
            'type': 'structure' if level else type
        }
        return d

    @classmethod
    def create_edit(cls, data, product_id, type_name):
        is_have_content = cls.query.filter(or_(cls.level == data.get('level'), cls.type == type_name)).first()

        data = cls().get_insert_data(data, product_id, type_name)
        if not is_have_content:
            content = cls(**data)
            db.session.add(content)
            return

        cls.update_model(is_have_content, data)
        return
