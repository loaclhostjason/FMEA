# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed

from ..base import BaseForm
from ..app import upload_video
from flask_login import  current_user
import os
from config import Config
import datetime


class SelectHelpDocForm(FlaskForm, BaseForm):
    time = StringField('时间')
    title = StringField('标题')
    submit = SubmitField('搜索')



class SelectHelpVideoForm(FlaskForm, BaseForm):
    time = StringField('时间')
    title = StringField('标题')
    submit = SubmitField('搜索')


class HelpDocForm(FlaskForm, BaseForm):
    title = StringField('标题:', validators=[DataRequired('标题不能空')])
    file = FileField('帮助文档:')
    submit = SubmitField('确定')

class HelpVideoForm(FlaskForm, BaseForm):
    title = StringField('标题:', validators=[DataRequired('标题不能空')])
    file = FileField('帮助视频:', validators=[FileRequired('不允许为空'), FileAllowed(upload_video, '只允许视频格式')])
    submit = SubmitField('确定')

    def __save_video(self):
        upload_files_path = os.path.join(Config.UPLOADS_DEFAULT_DEST, datetime.datetime.now().strftime('%Y%m%d'))

        filename_list = os.path.splitext(self.file.data.filename)
        now = datetime.datetime.now().strftime('%H%M%S')
        save_filename = filename_list[0] + '_' + now + filename_list[-1]

        file = upload_video.save(self.file.data, folder=upload_files_path, name=save_filename)
        return file

    def get_video_form(self):
        d = {
            'title': self.title.data,
            'file': self.__save_video(),
            'file_name': self.file.data.filename,
            'type': 'video',
            'user_id': current_user.get_id()
        }
        return d
