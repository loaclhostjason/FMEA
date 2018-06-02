# coding:utf-8

from .. import db
from models.help.doc import HelpFilesMixin
import os
from flask import current_app
from flask_login import current_user
from .func import *


class HelpFiles(HelpFilesMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(HelpFiles, self).__init__(*args, **kwargs)

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
            model = model.filter(cls.title.like( '%' + str(params['title']).strip() + '%'))
        return model.all()

    @classmethod
    def edit_or_create_doc(cls, form_data, doc):
        form_data['user_id'] = current_user.get_id()
        if not doc:
            doc = cls(**form_data)
            db.session.add(doc)
            return

        if form_data.get('file'):
            base_path = os.path.join(current_app.config['UPLOAD_DOC_DIR'], doc.time.strftime('%Y%m%d'))
            del_os_filename(base_path, doc.file)
            doc.file = form_data['file']
            doc.file_name = form_data.get('file_name')

        db.session.add(doc)
        return

    @classmethod
    def edit_or_create_video(cls, form_data, video):
        if not video:
            doc = cls(**form_data)
            db.session.add(doc)
            return

        del_file(video.file)
        video.tile = form_data['tile']
        video.file = form_data['file']
        video.file_name = form_data['file_name']
        db.session.add(video)
        return
