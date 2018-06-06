# coding:utf-8
from . import manage
from flask import jsonify, request
from flask_login import login_required
import json

from ..main.models import Attr
from .models import *
from .. import db


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
    if request.method == 'POST':
        form_data = request.form.to_dict()
        name_number = form_data.get('name_number')
        product_id = form_data.get('product_id')
        type = form_data.get('type')
        action_type = form_data.get('action_type')
        assess = form_data.get('assess')

        if not product_id or not name_number:
            return jsonify({'success': False, 'message': '参数不对'})

        if not form_data.get('name'):
            return jsonify({'success': False, 'message': '名称不能为空'})

        Tool.remove_key(form_data, ['product_id', 'name_number', 'type', 'action_type', 'assess'])
        d = {
            'product_id': product_id,
            'name_number': name_number,
            'content': json.dumps(form_data),
            'type': type,
            'action_type': action_type,
            'assess': assess,
        }
        assess = ProductAssess.query.filter_by(product_id=product_id, name_number=name_number, type=type, action_type=action_type).first()

        ProductAssess.create_edit(d, assess)

        return jsonify({'success': True, 'message': '更新成功'})

    product_id = request.args.get('product_id')
    name_number = request.args.get('name_number')
    type = request.args.get('type')
    action_type = request.args.get('action_type')
    assess = request.args.get('assess')

    assess = ProductAssess.query.filter_by(product_id=product_id, name_number=name_number, type=type, action_type=action_type, assess=assess).first()
    content = None
    if assess:
        content = json.loads(assess.content)
    return jsonify({'success': True, 'data': content})
