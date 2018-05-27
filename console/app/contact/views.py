# coding: utf-8
from . import contact
from flask import render_template


@contact.route('/ways')
def contract_way():
    return render_template('contact/ways.html')
