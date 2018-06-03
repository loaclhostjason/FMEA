from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email
from ..base import BaseForm
from flask import request
from flask_login import current_user


class ContactForm(FlaskForm, BaseForm):
    address = StringField('地址:', validators=[DataRequired('地址不能为空')])
    email = StringField('邮箱:', validators=[DataRequired('邮箱不能为空'), Email('邮箱格式不对')])
    phone = StringField('电话:', validators=[DataRequired('电话不能为空')])
    fax = StringField('传真:', validators=[DataRequired('传真不能为空')])

    def __init__(self):
        super(ContactForm, self).__init__()
        self.required_form()


class AttrForm(FlaskForm, BaseForm):
    name = StringField('节点名称:')
    type = SelectField('树类型:', coerce=str)
    content = StringField()

    def __init__(self):
        super(AttrForm, self).__init__()
        from models.industry.product import AttrType
        print(list(AttrType))
        self.type.choices = [(v.name, v.value) for v in list(AttrType)]

    def get_content(self):
        field_key = [
            'field',
            'field_zh',
            'required',
        ]
        field = request.form.getlist('field')
        if not field:
            return

        result = list()
        for index, val in enumerate(field):
            d = dict()
            for k in field_key:
                try:
                    dict_value = request.form.getlist(k)[index]
                    if dict_value:
                        d[k] = dict_value
                except Exception:
                    pass
            result.append(d)
        return result


class AttrExtraForm(FlaskForm, BaseForm):
    name_number = StringField('编号:')
    extra = HiddenField(default=True)
    content = StringField()
    username = StringField()

    def __init__(self):
        super(AttrExtraForm, self).__init__()
        self.username.data = current_user.username

    def get_content(self):
        field_key = [
            'field',
            'field_zh',
            'required',
        ]
        field = request.form.getlist('field')
        if not field:
            return

        result = list()
        for index, val in enumerate(field):
            d = dict()
            for k in field_key:
                try:
                    dict_value = request.form.getlist(k)[index]
                    if k == 'required':
                        d[k] = bool(dict_value == 'y')
                    else:
                        if dict_value:
                            d[k] = dict_value
                except Exception:
                    pass
            result.append(d)
        return result
