# coding:utf-8
from . import manage
from flask import jsonify, request
from flask_login import login_required
import json

from ..main.models import Attr, ProductTree
from .models import *
from .. import db
from .func import get_all_func


@manage.route('/attr/content/add', methods=['POST'])
@login_required
def add_attr_content():
    # add 参数
    product_id = request.args.get('product_id')
    name_number = request.form.get('name_number')
    level = request.form.get('level')
    type = request.form.get('type_name')

    if not product_id or not name_number:
        return jsonify({'success': False, 'message': '提交参数缺失'})

    form_data = request.form.to_dict()

    attr = Attr.query.filter_by(name_number=name_number).first()
    if not attr:
        attr = Attr.query.filter(or_(Attr.level == level if level else False, Attr.type == type)).first()

    print(attr)
    content = json.loads(attr.content) if attr and attr.content else []
    result = [(info['field'], info['field_zh']) for info in content if info.get('required')]

    if result:
        for r, r_name in result:
            if not form_data.get(r):
                return jsonify({'success': False, 'message': '请检查【%s】，是否必须填写' % r_name})

    AttrContent.create_edit(form_data, product_id, name_number)
    return jsonify({'success': True, 'message': '更新成功'})


@manage.route('/product/assess/create_edit', methods=['GET', 'POST'])
@login_required
def create_edit_assess():
    product_id = request.args.get('product_id')
    func_relation_id = request.args.get('func_relation_id')
    type = request.args.get('type')
    action_type = request.args.get('action_type')

    if request.method == 'POST':
        form_data = request.form.to_dict()

        if not product_id or not func_relation_id:
            return jsonify({'success': False, 'message': '参数不对'})

        d = {
            'product_id': product_id,
            'func_relation_id': func_relation_id,
            'content': json.dumps(form_data),
            'type': type,
            'action_type': action_type,
        }
        assess = ProductAssess.query.filter_by(product_id=product_id, func_relation_id=func_relation_id, type=type,
                                               action_type=action_type).first()

        ProductAssess.create_edit(d, assess)
        return jsonify({'success': True, 'message': '更新成功'})

    assess = ProductAssess.query.filter_by(product_id=product_id, func_relation_id=func_relation_id, type=type,
                                           action_type=action_type).first()
    content = None
    if assess:
        content = json.loads(assess.content)
    return jsonify({'success': True, 'data': content})


@manage.route('/edit/tree', methods=['GET', 'POST'])
def edit_tree_func_fail():
    type = request.args.get('type')
    id = request.args.get('id')
    key = request.args.get('key')
    product_id = request.args.get('product_id')

    func_id = request.args.get('func_id')
    if not type or not id or not product_id:
        return jsonify({'success': True, 'data': []})

    old_product_tree = ProductTree.query.filter_by(type=type, product_id=product_id, product_relation_id=id,
                                                   func_id=func_id).first()

    result = get_all_func(id, product_id, type, False, func_id)
    if request.method == 'POST':
        if old_product_tree:
            result = json.loads(old_product_tree.content)
        for r in result:
            if r['key'] == key:
                r['is_show'] = not r['is_show']

        old_product_tree.content = json.dumps(result)
        old_product_tree.is_show = not old_product_tree.is_show
        return jsonify({'success': True, 'data': result})

    if not old_product_tree:
        # add new
        new_dict = {
            'type': type,
            'product_relation_id': id,
            'func_id': func_id,
            'content': json.dumps(result),
            'product_id': product_id
        }
        db.session.add(ProductTree(**new_dict))
    else:
        result = json.loads(old_product_tree.content)
    return jsonify({'success': True, 'data': result})
