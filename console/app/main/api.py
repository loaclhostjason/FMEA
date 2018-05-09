# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash
from flask_login import login_required

from . import main
from .forms import *
from .. import db
from .models import *
from ..read_config import ReadConfig


@main.route('/file/product/create', methods=['POST'])
@login_required
def create_file_product():
    form_data = request.form.to_dict()
    if not form_data.get('config_name'):
        return jsonify({'success': False, 'message': '没有选择配置文件'})

    config_data = ReadConfig().read_config_data(form_data['config_name'])

    product = Product.query.filter_by(config_name=form_data['config_name']).first()
    if product:
        return jsonify({'success': False, 'message': '添加过，请编辑'})

    d = dict({'config_name': form_data['config_name'], **config_data})
    db.session.add(Product(**d))
    return jsonify({'success': True, 'message': '更新成功', 'config_name': form_data['config_name']})
