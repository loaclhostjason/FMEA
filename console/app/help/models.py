# coding:utf-8

from .. import db
from models.help.doc import HelpDocMixin
import os
from flask import current_app
from flask_login import current_user
from .func import *


class HelpDoc(HelpDocMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(HelpDoc, self).__init__(*args, **kwargs)

    @staticmethod
    def __get_start_end_date(range_date):
        if not range_date:
            raise ValueError('日期格式不对')

        try:
            date_list = range_date.split(' - ')
            start_time = '%s %s' % (date_list[0], '00:00:00')
            end_time = '%s %s' % (date_list[1], '23:59:59')
        except:
            start_time = end_time = False
        return start_time, end_time

    @classmethod
    def filter_params(cls, model, params):
        if not params:
            return model.all()

        if params.get('time'):
            start_time, end_time = cls.__get_start_end_date(params['time'])
            model = model.filter(cls.time > start_time, cls.time <= end_time)

        if params.get('title'):
            model = model.filter(cls.title == params['title'])
        return model.all()

    @classmethod
    def edit_or_create(cls, form_data, doc):
        form_data['user_id'] = current_user.get_id()
        if not doc:
            doc = cls(**form_data)
            db.session.add(doc)
            return

        if form_data.get('file'):
            base_path = os.path.join(current_app.config['UPLOAD_DOC_DEST'], doc.time.strftime('%Y%m%d'))
            del_os_filename(base_path, doc.file)
            doc.file = form_data['file']
            doc.file_name = form_data.get('file_name')

        db.session.add(doc)
        return
