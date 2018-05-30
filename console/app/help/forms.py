# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired
from wtforms import ValidationError

from ..base import BaseForm


class SelectHelpDocForm(FlaskForm, BaseForm):
    time = StringField('时间')
    title = StringField('标题')
    submit = SubmitField('搜索')


class HelpDocForm(FlaskForm, BaseForm):
    title = StringField('标题')
    file = FileField('帮助文档')
    submit = SubmitField('确定')
