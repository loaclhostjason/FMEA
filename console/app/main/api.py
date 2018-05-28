# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash
from flask_login import login_required, current_user

from . import main
from .forms import *
from .. import db
from .models import *
from ..read_config import ReadConfig

from .func import get_func_relation, get_failure_relation

'''
我的文件 delete
'''


@main.route('/file/product/delete/<int:id>', methods=['POST'])
def delete_file(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    return jsonify({'success': True, 'message': '删除成功'})


'''
我的文件 create
'''


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


'''
我的文件 树
'''


@main.route('/file/tree')
@login_required
def get_file_tree():
    result = {
        'nodedata': [],
        'linkdata': [],
    }

    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({'success': False, 'message': '没有获取到配置文件信息'})

    product = Product.query.get_or_404(product_id)
    result['nodedata'].append({'name': product.name, 'key': product_id, 'level': product.level + 1})

    realtion = product.product_relation
    link_data = []
    for rl in realtion:
        # if rl.parent_id != product_id:
        link_data.append({'from': rl.parent_id, 'to': rl.id})
        result['nodedata'].append({'name': rl.name, 'key': rl.id, 'level': rl.level + 1})

    result['linkdata'] = link_data
    return jsonify({'success': True, 'data': result})


@main.route('/file/func/failure/tree')
@login_required
def get_file_func_tree():
    result = {
        'nodedata': [],
        'linkdata': [],
    }

    type = request.args.get('type')

    if type == 'func':
        product_relation_id = request.args.get('product_relation_id')
        result = get_func_relation(result, product_relation_id)

    if type == 'failure':
        func_relation_id = request.args.get('func_relation_id')

        func_relation = FuncRelation.query.get_or_404(func_relation_id)
        result = get_func_relation(result, func_relation.product_relation_id)

        result = get_failure_relation(result, func_relation_id)

    return jsonify({'success': True, 'data': result})


'''
我的文件 儿子节点添加
'''


@main.route('/file/tree/content/add/<int:id>', methods=['POST'])
@login_required
def add_file_tree_content(id):
    form_data = request.form.to_dict()

    if not form_data.get('content'):
        return jsonify({'success': False, 'message': '内容不能为空'})

    d = {
        'parent_id': form_data.get('parent_id') or id,
        'product_id': id,
        'level': int(form_data['level']) if form_data.get('level') else None
    }

    product_relation_id = None
    func_relation_id = None
    if form_data.get('type') == 'func':
        product_relation_id = FuncRelation.add_func_relation(d, form_data.get('content'))
    elif form_data.get('type') == 'failure':
        func_relation_id = FailureRelation.add_fail_relation(d, form_data.get('content'))
    else:
        ProductRelation.add_product_relation(d, form_data.get('content'))
    return jsonify({'success': True, 'type': form_data.get('type'), 'product_relation_id': product_relation_id, func_relation_id: func_relation_id})
