from models.temps.temps import TempsMixin
from .. import db


class Temps(TempsMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(Temps, self).__init__(*args, **kwargs)

    @classmethod
    def insert_tmeps(cls):
        old = cls.query.first()
        if old:
            return

        first_data = {
            'name_number': '0',
            'name': '名称0',
            'level': None,
            'parent_id': None,
            'number': 1
        }
        init_data = cls(**first_data)
        db.session.add(init_data)
        db.session.flush()
        parent_id = init_data.id

        data = [
            {
                'name_number': '1',
                'name': '名称1',
                'level': 1,
                'number': 1
            },
            {
                'name_number': '1.1',
                'name': '名称2',
                'level': 2,
                'number': 1
            },
            {
                'name_number': '1.2',
                'name': '名称3',
                'level': 2,
                'number': 2
            }]

        for d in data:
            d['parent_id'] = parent_id
            db.session.add(cls(**d))
            db.session.commit()

        return
