# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash
from flask_login import login_required, current_user

from . import main
from .forms import *
from .. import db
from .models import *
from ..read_config import ReadConfig


@main.route('/file/product/delete/<int:id>', methods=['POST'])
def delete_file(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    return jsonify({'success': True, 'message': '删除成功'})


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

    d = dict({'config_name': form_data['config_name']}, **config_data)

    d['user_id'] = current_user.get_id()
    add_product = Product(**d)
    db.session.add(add_product)
    db.session.flush()

    product_id = add_product.id
    return jsonify({'success': True, 'message': '更新成功', 'product_id': product_id})


@main.route('/file/tree')
@login_required
def get_file_tree():
    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({'success': False, 'message': '没有获取到配置文件信息'})

    product = Product.query.get_or_404(product_id)
    product_info = {"name": product.name}

    result = {
        'nodedata': [],
        'linkdata': [],
    }

    result['nodedata'].append(product_info)
    result['linkdata'] = []
    return jsonify({'success': True, 'data': result})
