# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from ..models import User
from ..base import BaseForm

from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm, BaseForm):
    email = StringField(validators=[DataRequired(message='用户名不能为空！'), Email('邮箱地址格式不对')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空！')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

    def __init__(self):
        super(LoginForm, self).__init__()
        render_kw_dict = {
            'email': {'placeholder': '邮箱'},
            'password': {'placeholder': '登录密码'},
        }
        self.required_form(**render_kw_dict)


class RegisterForm(FlaskForm, BaseForm):
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Email('邮箱地址格式不对')])
    username = StringField(validators=[DataRequired('用户名不能为空')])
    password = PasswordField(validators=[DataRequired(message='新密码不能为空'), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField(validators=[DataRequired(message='确认密码不能为空')])
    submit = SubmitField('注册')

    def __init__(self):
        super(RegisterForm, self).__init__()
        render_kw_dict = {
            'email': {'placeholder': '邮箱'},
            'username': {'placeholder': '用户名'},
            'password': {'placeholder': '新密码'},
            'password2': {'placeholder': '确认密码'},
        }
        self.required_form(**render_kw_dict)
