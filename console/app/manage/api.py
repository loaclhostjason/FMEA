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
    product_id = request.args.get('product_id')
    type = request.form.get('type_name')
    if not product_id:
        return jsonify({'success': False, 'message': '提交参数缺失'})

    form_data = request.form.to_dict()

    attr = Attr.query.filter_by(level=form_data.get('level')).first()

    if not attr:
        return jsonify({'success': False, 'message': '没有记录，联系管理员'})

    content = json.loads(attr.content)
    result = [(info['field'], info['field_zh']) for info in content if info.get('required')]

    if result:
        for r, r_name in result:
            if not form_data.get(r):
                return jsonify({'success': False, 'message': '请检查【%s】，是否必须填写' % r_name})

    AttrContent.create_edit(form_data, product_id, type)
    return jsonify({'success': True, 'message': '更新成功'})
