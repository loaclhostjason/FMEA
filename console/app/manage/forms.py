from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email
from ..base import BaseForm


class ContactForm(FlaskForm, BaseForm):
    address = StringField('地址:', validators=[DataRequired('地址不能为空')])
    email = StringField('邮箱:', validators=[DataRequired('邮箱不能为空'), Email('邮箱格式不对')])
    phone = StringField('电话:', validators=[DataRequired('电话不能为空')])
    fax = StringField('传真:', validators=[DataRequired('传真不能为空')])

    def __init__(self):
        super(ContactForm, self).__init__()
        self.required_form()
