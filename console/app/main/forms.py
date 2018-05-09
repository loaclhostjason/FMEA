# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from ..models import User
from ..base import BaseForm

from ..read_config import ReadConfig


class CreateProductForm(FlaskForm, BaseForm):
    config_name = SelectField('选择配置文件', coerce=str, validators=[DataRequired(message='文件名不能空')])

    def __init__(self, *args, **kwards):
        super(CreateProductForm, self).__init__(*args, **kwards)

        paths = ReadConfig().get_all_config()
        print(111, paths)
        self.config_name.choices = [(path['filename'], path['filename']) for path in paths] if paths else []
