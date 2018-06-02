from . import manage
from flask_login import login_required
from flask import render_template, flash, redirect, url_for, request
from ..decorators import role_required
from ..contact.models import ContactWay
from .forms import *
from ..base import Check
from .. import db


@manage.route('/config/list')
@login_required
@role_required
def config_list():
    return render_template('manage/config.html')


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
