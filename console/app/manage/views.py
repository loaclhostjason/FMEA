from . import manage
from flask_login import login_required
from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from ..decorators import role_required
from ..contact.models import ContactWay
from .forms import *
from ..base import Check
from .. import db
from ..main.models import Attr
import json


@manage.route('/config/list')
@login_required
@role_required
def config_list():
    attrs = Attr.query.all()
    return render_template('manage/config.html', attrs=attrs)


@manage.route('/config/attr/delete/<int:id>', methods=['POST'])
@login_required
@role_required
def delete_config_attr(id):
    attr = Attr.query.filter_by(id=id).first()
    if not attr:
        return jsonify({'success': False, 'messgae': '没有此记录'})
    db.session.delete(attr)
    return jsonify({'success': True, 'messgae': '删除成功'})


@manage.route('/attr/edit', methods=['GET', 'POST'])
@login_required
@role_required
def edit_attr():
    form = AttrForm()
    id = request.args.get('id')
    attr_info = Attr.query.get_or_404(id)
    if not attr_info:
        abort(404)

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        form_data = form.get_form_data()
        content = form.get_content()
        new_form_data = dict({'content': json.dumps(content)}, **form_data)
        Attr.edit(new_form_data, attr_info)
        flash({'success': '更新成功'})
        return redirect(url_for('.config_list'))

    form.set_form_data(attr_info)
    form.type.data = attr_info.type.name
    return render_template('manage/edit_attr.html', attr_info=attr_info, form=form)


@manage.route('/extra/attr/create_edit', methods=['GET', 'POST'])
@login_required
@role_required
def create_edit_extra_attr():
    form = AttrExtraForm()
    id = request.args.get('id')
    attr_info = Attr.query.filter_by(id=id).first()

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        form_data = form.get_form_data()
        form_data['extra'] = bool(form_data.get('extra') == 'True')
        content = form.get_content()
        new_form_data = dict({'content': json.dumps(content), **form_data})
        print(new_form_data)
        Attr.create_edit_extra(new_form_data, attr_info)
        flash({'success': '更新成功'})
        return redirect(url_for('.config_list'))

    if attr_info:
        form.set_form_data(attr_info)
    return render_template('manage/create_edit_extra_attr.html', attr_info=attr_info, form=form)


@manage.route('/contact', methods=['GET', 'POST'])
@login_required
@role_required
def manage_contact():
    form = ContactForm()
    contact = ContactWay.query.first()

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        form.populate_obj(contact)
        db.session.add(contact)
        flash({'success': '更新成功'})
        return redirect(request.url)

    if contact:
        form.set_form_data(contact)
    return render_template('manage/contact.html', contact=contact, form=form)
