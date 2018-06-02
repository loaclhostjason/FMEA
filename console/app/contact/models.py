from .. import db
from models.contact.contact import ContactWayMixin


class ContactWay(ContactWayMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(ContactWay, self).__init__(*args, **kwargs)

    @classmethod
    def insert_data(cls):
        d = {
            'address': '中华人民共和国',
            'email': 'admin@qq.com',
            'phone': '12345678901',
            'fax': '12345678901',
        }
        old_contact = cls.query.first()
        if old_contact:
            return

        contact = cls(**d)
        db.session.add(contact)
        db.session.commit()
        return
