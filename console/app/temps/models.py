from models.temps.temps import TempsMixin
from .. import db


class Temps(TempsMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(Temps, self).__init__(*args, **kwargs)

    @classmethod
    def insetrt_tmeps(cls):
        first_data = {
            'name_number': '0',
            'name': '模板一',
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
                'name': 'sss',
                'level': 1,
                'parent_id': 1,
                'product_id': 3,
                'number': 1
            },
            {
                'name_number': '1.1',
                'name': 'S',
                'level': 2, 'parent_id': 2,
                'product_id': 3,
                'number': 1
            },
            {
                'name_number': '1.2',
                'name': 'D',
                'level': 2,
                'parent_id': 2,
                'number': 2
            }]
