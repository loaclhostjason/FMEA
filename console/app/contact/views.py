# coding: utf-8
from . import contact
from flask import render_template
from .models import *
from flask_login import login_required


@contact.route('/ways')
@login_required
def contract_way():
    contact = ContactWay.query.first()
    return render_template('contact/ways.html', contact=contact)
